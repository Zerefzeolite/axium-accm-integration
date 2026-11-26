# Personal development baseline — review request, not admission receipt

Owner has clarified the purpose is personal project development and continuation, not company-exclusive operational use, and has authorized investigating and proposing security patches if required. Scope of this candidate: offline, disposable, credential-free development/test of unchanged published sm-action v3.0.1 source. No distribution, operational use, real credentials, provider access or production admission. The owner statement does not itself settle SDK operational licensing, permit modification of restricted SDK components, or replace independent acceptance.

## Exact input evidence

- Inventory run 45795132771 / job 139823737066 succeeded; 387/387 registry package checksums matched original Cargo.lock, 186 installed Ubuntu packages, 96 Debian archives; vendored file checksum checks passed.
- Proposed manifest is the exact log record plus final LF; SHA256 84ffa90efe3981649d58c7da51bb9ff5ddf13086aed097b0922c43e980ba9b3b. It is **not approved while on a review branch**. Protected main merge and recorded independent review are required before one build-mode dispatch.
- Original source commit 1238aae8fc64b212641190a9227c8a734ab1a793, tree ba5c80c1ba7d268cb91e34b153f161646737d9ec, lock SHA256 cf301ce7de2e66b03cfbe7174b7a91e058f367a3c0bdf5cf5a4bbb52ba92445a, six exact source files. No lockfile changes.
- Workflow retains exact environment manifest comparison, restricted network-none non-root container, read-only source/vendor/toolchain, no credentials, capability drops, seccomp, and native release/test/version checks. Adds active Linux feature tree before compilation and sanitized compiler/test logs. No new provider or execution permission.

## Security review and patch candidates

Pinned RustSec DB commit c9f6c91a44dbad9d71742329e9df061279f9c4be. Registry versions are inventory matches, not proof of runtime reachability. Preliminary priority list:

| Package | Locked | Candidate minimum for reviewed advisory | Advisory |
|---|---|---|---|
| rustls-webpki | 0.103.13 | 0.103.16 | RUSTSEC-2026-0382 (certificate verification) |
| rustls | 0.23.40 | 0.23.46 | RUSTSEC-2026-0285, 0346, 0348, 0349 |
| h2 | 0.4.14 | 0.4.16 | RUSTSEC-2026-0258 |
| quinn-proto | 0.11.14 | 0.11.19 | RUSTSEC-2026-0185, 0523, 0524 |
| url | 2.5.8 | 2.5.9 | RUSTSEC-2026-0592 |
| libsqlite3-sys | 0.37.0 | 0.39.0 | RUSTSEC-2026-0459; bundled SQLite and feature dependent |
| anyhow | 1.0.102 | 1.0.103 | RUSTSEC-2026-0190 informational unsoundness |
| tokio | 1.50.0 | supported patched line per advisory | RUSTSEC-2026-0386 informational unsoundness |
| chrono | 0.4.45 | no fix stated | RUSTSEC-2026-0543 unmaintained |

Not an exhaustive scan; full graph/advisories, build scripts (67 declarations) and proc macros (37) remain under review. Confirm actual Linux features before recommending changes. Review patched version availability and dependency constraints; use separate candidate lockfile with minimal official upstream upgrades and compare results. Do not silently modify SDK source or assert any fix is complete. Avoid a broad update. Separate permission/license review for changed or redistributed SDK components.

## Required review and dispatch

An independent reviewer must assess the exact inputs, the remaining build-time code risk and containment, and explicitly accept or reject one disposable development-only offline build. The review should identify any missing controls and require corrections before admission where material. A protected branch approval is necessary but does not substitute for independent technical acceptance. The operator must not run build mode until that acceptance is recorded and the exact reviewed manifest is on signed main. No credentials or published artifacts. Native success is not release provenance, a full advisory clearance, or credential admission. After baseline results, perform feature-based patch assessment, independently reviewed changes, repeat build/test and provenance/licensing disposition. 
