# Container-native build candidate

Run 45792664193 passed the pinned Ubuntu amd64 image isolation and Rust/Cargo installation checks. This workflow uses the same base manifest and image config, signed Rust channel and archive, and observed compiler executable digests. The previous host-namespace candidate and credential-bearing workflow are unchanged.

## Inputs and operation

- Public upstream commit 1238aae8fc64b212641190a9227c8a734ab1a793 and exact tree, six build-input blobs, unchanged Cargo.lock (388 packages including the root, 387 checksummed registry crates).
- Ubuntu archive snapshot 20261125T000000Z, signed apt metadata and downloaded .deb hashes, package and native tool inventories. The package seed includes C/C++ compiler, linker, pkg-config, SQLite and OpenSSL development headers, certificate bundle, Python, Git and Perl. No mutable latest package sources or unauthenticated packages. Availability and package closure are unverified until inventory mode runs.
- The package image is built locally in the disposable GitHub VM with no secret build arguments or private inputs. The network-enabled vendor stage only downloads packages into its disposable mounts. The offline build container has network none, read-only root, read-only source/toolchain/vendor, non-root uid, no capabilities, no-new-privileges, default seccomp, no Docker socket and a bounded dedicated writable work directory.
- Inventory mode validates every vendored file against Cargo checksum metadata, binds package archive checksums to Cargo.lock, records build-script/proc-macro and license declarations, and prints exact manifest and inventories. This is not a source or security audit: a subsequent reviewer must inspect actual build scripts, proc macros, effective dependency graph, advisories, licensing and image/package closure. Cargo validates registry package checksums during vendoring; local file checks verify the resulting tree.
- Build mode requires matching exact manifest bytes at qualification/APPROVED_CONTAINER_BUILD.json on protected main and the exact digest dispatch input. That file is deliberately absent. A manifest must not be treated as proof of genuine independent acceptance; acceptance is separately recorded. Source build, tests and version checks are offline. Release uses upstream static CRT flags; tests use dynamic CRT as upstream. Native version probe has empty private command files.
- Build receipt records executable size and digest, tests and version, not a signed attestation or proof of original publisher binary equivalence. Repeat independently using the same measured inputs before candidate admission; investigate differing results. Binary is not published or retained by this workflow. Attestation and license-approved artifact retention remain separate. No provider authentication or private data is permitted.

## Review sequence

1. Review signed workflow and run inventory only.
2. Verify actual input evidence and dependency closure, including license/advisory review. Authorize exact manifest under protected main controls; do not approve solely on an owner dispatch or script-generated digest.
3. Run build, verify native tests and executable evidence, repeat independently. No credential-bearing use is authorized by this work.
