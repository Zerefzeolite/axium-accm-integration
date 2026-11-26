# Credential-free pinned-source build candidate

Status: draft for independent technical review; includes a manual hosted workflow candidate; not merged or admitted to credential use.

## Exact source and proposed toolchain

- Upstream: https://github.com/bitwarden/sm-action/tree/1238aae8fc64b212641190a9227c8a734ab1a793
- Commit: 1238aae8fc64b212641190a9227c8a734ab1a793 (upstream commit is unsigned).
- Tree: ba5c80c1ba7d268cb91e34b153f161646737d9ec.
- Cargo.lock blob: 279d24b39d2978eb3ab5944e6e56f2a8db8428a7.
- 388 package entries: 387 registry entries with 64-hex checksums, one root package, zero git entries.
- Proposed compiler: Rust 1.98.0, based on upstream later commit bbc9efefcc75042010c202240961853650c88979. It is not established as the original release compiler.
- Target: x86_64-unknown-linux-gnu.
- Original release SHA-256: fa998e9db775d5c7bdbc0fd8840ac6474a8348cdc989176c5ce24c3d09045752 (comparison only).

## Before execution

1. Independently review the exact candidate, public upstream Rust sources, all build scripts/proc macros and target dependency closure; audit advisories and SDK licensing before redistribution.
2. Confirm the build is in a new disposable non-root Linux environment with no real or synthetic provider credentials, private source, host mounts, shared caches or privileged broker access. Verify supported network namespace isolation. No existing credential-bearing environment or runner is suitable by assumption.
3. Authenticate the exact Rust distribution manifest and archive hashes through the official distribution channel; verify installed compiler, Cargo, stdlib, linker, system libraries, OS image and ancillary tool hashes. Record those pins in the independently reviewed admission manifest. The script checks the supplied manifest and executable digests, but does not verify reviewer authority or the full environment itself. The admission manifest and command arguments cannot substitute for genuine independent acceptance.
4. Permit only public source and dependency acquisition in the isolated preparation phase. No arbitrary upstream workflows are run. Review vendored content, Cargo checksums and native build dependencies before treating any executable as trustworthy.
5. Run the candidate with an externally verified compiler directory and exact approved digests. The build uses fresh Cargo home, Git config and target directory, vendored locked packages, frozen offline build and tests inside a separate network namespace. An unavailable namespace, incorrect source, wrong toolchain, dependency error, version mismatch or modified checkout fails closed.
6. Capture actual build/test exit status, source/environment pins, native version, executable digest and size. Independently rerun on a second clean environment with equivalent exact pins; compare candidate digests, investigate any mismatch. Native version is not a provider authentication test. Retain evidence, destroy temporary hosts/worktrees after approved evidence handoff.

## Provenance and admission

The original publisher's release remains held for provenance. A matching new digest would be useful evidence; a different digest does not automatically disqualify a separately reviewed new binary. Neither result alone is a release approval.

A separately reviewed public build-only attestation lane may be proposed using a pinned and specifically allowlisted attestation action, a restricted OIDC signing job with no provider credentials, and digest/identity verification. No attestation workflow, artifact upload, Actions settings change, attestation, or executable publication is included here. The current synthetic-qualification workflow and SECURITY.md remain untouched. Any later publication needs a separate license and authority review.

No new credential-bearing run or consumer is authorized by this draft. Effective single-fixture provider isolation, genuinely independent human acceptance, durable one-use dispatch and existing synthetic cleanup controls remain separate prerequisites. Never attach or log tokens, private project details or actual credential identifiers in a public build.

## Hosted Ubuntu qualification lane

The new source-qualification.yml is manual-dispatch only, repository/owner/main/first-attempt restricted, standard ubuntu-24.04, token permissions empty, no external Actions or provider secrets, no artifact publication. It verifies the official Rust 1.98.0 channel manifest against the pinned Rust signing-key fingerprint and strong digest algorithm, then verifies the archive and uses a disposable isolated prefix. The runner image label is not immutable; the preflight records image version, OS, kernel, package inventory, tool hashes, toolchain tree, and a native network-namespace probe. Installation logs are excluded from the toolchain tree digest because they can contain random paths. This is a measured environment, not proof of every system library byte or full process isolation. No weakening of host AppArmor/user-namespace restrictions is permitted. The preflight does not build or authenticate.

Build mode additionally requires the exact preflight environment JSON to be independently reviewed and committed as qualification/APPROVED_HOSTED_ENVIRONMENT.json on protected main, with matching dispatch digest. That file is intentionally absent in this candidate. The exact build script blob is pinned. Hosted image or toolchain drift fails closed; if host image churn or nondeterminism prevents stable qualification, revise the runner approach under separate review rather than relax the match. Successful build logs provide a digest/version/test receipt, not a retained artifact or signed provenance. Candidate binaries and temporary files are not published; retention and attestation require a separately reviewed lane. Neither the approved JSON nor owner dispatch alone constitutes an independent acceptance record.
