#!/usr/bin/env python3
"""Credential-free candidate only. Do not run on a credential-bearing host."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

COMMIT = "1238aae8fc64b212641190a9227c8a734ab1a793"
TREE = "ba5c80c1ba7d268cb91e34b153f161646737d9ec"
UPSTREAM = "https://github.com/bitwarden/sm-action.git"
TOOLCHAIN = "1.98.0"
TARGET = "x86_64-unknown-linux-gnu"
ORIGINAL = "fa998e9db775d5c7bdbc0fd8840ac6474a8348cdc989176c5ce24c3d09045752"
PINS = {
    "Cargo.toml": "570832c893c2eafe6a918329c5510b5810245902",
    "Cargo.lock": "279d24b39d2978eb3ab5944e6e56f2a8db8428a7",
    "src/main.rs": "2ca8921c939df8b53902a93aae162b06562c5ee7",
    "src/config.rs": "eed4ce7a14f4249be82189f1b2f1df4c6d6e271d",
    "src/ci.rs": "08e184384973134e68bad14fe8d1d4ec4af25f72",
    "LICENSE": "e72bfddabc15be5718a7cc061ac10e47741d8219",
}

def require(condition, message):
    if not condition:
        raise SystemExit(message)

def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def run(args, env, cwd, timeout=120, capture=False):
    result = subprocess.run(
        [str(x) for x in args], env=env, cwd=cwd, check=True,
        timeout=timeout, text=True, stdout=subprocess.PIPE if capture else None,
        stdin=subprocess.DEVNULL,
    )
    return result.stdout.strip() if capture else ""

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--toolchain-dir", required=True, type=Path,
                   help="Reviewed isolated toolchain installation; no rustup shim.")
    p.add_argument("--rustc-sha256", required=True)
    p.add_argument("--cargo-sha256", required=True)
    p.add_argument("--admission-receipt", required=True, type=Path,
                   help="Exact independently reviewed build environment manifest.")
    p.add_argument("--admission-sha256", required=True)
    a = p.parse_args()
    require(os.uname().sysname == "Linux" and os.uname().machine == "x86_64",
            "Linux x86_64 required")
    require(os.geteuid() != 0, "Non-root disposable host identity required")
    for value in (a.rustc_sha256, a.cargo_sha256, a.admission_sha256):
        require(re.fullmatch("[0-9a-f]{64}", value), "Invalid reviewed digest")
    # Digest check is byte binding, NOT proof of reviewer identity or authorization.
    require(a.admission_receipt.is_file() and
            digest(a.admission_receipt) == a.admission_sha256,
            "Build environment admission manifest mismatch")
    rustc = a.toolchain_dir.resolve() / "bin/rustc"
    cargo = a.toolchain_dir.resolve() / "bin/cargo"
    require(rustc.is_file() and cargo.is_file(), "Missing compiler or Cargo")
    require(digest(rustc) == a.rustc_sha256 and digest(cargo) == a.cargo_sha256,
            "Toolchain executable digest mismatch")
    root = Path(tempfile.mkdtemp(prefix="accm-source-build-"))
    print("DISPOSABLE_ROOT=" + str(root), flush=True)
    home = root / "home"
    cargo_home = root / "cargo-home"
    src = root / "src"
    target_dir = root / "target"
    for directory in (home, cargo_home, src, target_dir):
        directory.mkdir(mode=0o700)
    env = {
        "PATH": "/usr/bin:/bin", "HOME": str(home), "CARGO_HOME": str(cargo_home),
        "RUSTC": str(rustc), "CARGO_TARGET_DIR": str(target_dir),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": "/dev/null",
        "LC_ALL": "C", "TZ": "UTC", "CARGO_INCREMENTAL": "0",
    }
    version = run([rustc, "--version", "--verbose"], env, root, capture=True)
    require(version.splitlines()[0].startswith("rustc " + TOOLCHAIN + " "),
            "Unexpected compiler version")
    require("host: " + TARGET in version.splitlines(), "Unexpected compiler target")
    cargo_version = run([cargo, "--version"], env, root, capture=True)
    require(cargo_version.startswith("cargo " + TOOLCHAIN + " "),
            "Unexpected Cargo version")
    host_netns = os.readlink("/proc/self/ns/net")
    # Every compile/test/version command starts in a fresh network namespace.
    # If namespace creation or verification fails, no compile/test runs.
    def offline(args, timeout=120, capture=False):
        return run(
            ["/usr/bin/unshare", "--user", "--map-root-user", "--net", "--",
             "/bin/sh", "-eu", "-c",
             'test "$(readlink /proc/self/ns/net)" != "$1"; shift; exec "$@"',
             "sh", host_netns, *args],
            env, src, timeout, capture,
        )
    offline(["/bin/true"])
    git = "/usr/bin/git"
    run([git, "init", "-q"], env, src)
    run([git, "fetch", "--no-tags", "--depth=1", UPSTREAM, COMMIT], env, src, 180)
    run([git, "checkout", "--detach", "FETCH_HEAD"], env, src)
    require(run([git, "rev-parse", "HEAD"], env, src, capture=True) == COMMIT,
            "Source commit mismatch")
    require(run([git, "rev-parse", "HEAD^{tree}"], env, src, capture=True) == TREE,
            "Source tree mismatch")
    for path, pin in PINS.items():
        require(run([git, "hash-object", "--no-filters", path], env, src,
                    capture=True) == pin, "Source blob mismatch: " + path)
    require(not (src / ".cargo").exists(), "Unexpected upstream Cargo config")
    # Cargo's registry package checksums are bound by the original lockfile.
    # Network is allowed ONLY for fetching source and vendoring in the fresh host.
    vendor = root / "vendor"
    run([cargo, "vendor", "--locked", "--versioned-dirs", vendor],
        env, src, 900)
    config = cargo_home / "config.toml"
    config.write_text(
        '[source.crates-io]\nreplace-with = "vendored-sources"\n'
        '[source.vendored-sources]\ndirectory = ' + json.dumps(str(vendor)) + '\n'
        '[net]\noffline = true\n',
        encoding="utf-8",
    )
    env["CARGO_NET_OFFLINE"] = "true"
    offline([cargo, "build", "--release", "--frozen", "--target", TARGET], 1800)
    offline([cargo, "test", "--release", "--frozen", "--target", TARGET], 1800)
    binary = target_dir / TARGET / "release" / "sm-action"
    require(binary.is_file() and not binary.is_symlink(), "Build output missing")
    candidate_sha = digest(binary)
    # Upstream constructs its Actions runner before handling --version.
    # Use only local empty command files, never the actual CI command channels.
    command_env = root / "probe-env"
    command_output = root / "probe-output"
    command_env.touch(mode=0o600, exist_ok=False)
    command_output.touch(mode=0o600, exist_ok=False)
    env["GITHUB_ENV"] = str(command_env)
    env["GITHUB_OUTPUT"] = str(command_output)
    try:
        native_version = offline([binary, "--version"], capture=True)
    finally:
        env.pop("GITHUB_ENV")
        env.pop("GITHUB_OUTPUT")
    require(native_version == "3.0.1", "Unexpected native version")
    require(command_env.stat().st_size == 0 and command_output.stat().st_size == 0,
            "Unexpected native probe command output")
    require(digest(binary) == candidate_sha, "Binary changed during version probe")
    require(not run([git, "status", "--porcelain", "--untracked-files=all"],
                    env, src, capture=True), "Upstream checkout changed")
    receipt = {
        "source_commit": COMMIT, "source_tree": TREE, "target": TARGET,
        "rustc": version, "cargo": cargo_version, "rustc_sha256": a.rustc_sha256,
        "cargo_sha256": a.cargo_sha256, "environment_manifest_sha256": a.admission_sha256,
        "candidate_sha256": candidate_sha, "candidate_bytes": binary.stat().st_size,
        "original_release_sha256": ORIGINAL, "matches_original": candidate_sha == ORIGINAL,
        "native_version": native_version, "build_tests": "exit_zero",
        "scope": "credential-free candidate; not an attestation or admission",
    }
    (root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n",
                                      encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    print("CANDIDATE_BUILT_NOT_ADMITTED")

if __name__ == "__main__":
    main()
