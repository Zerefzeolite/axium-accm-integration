# R1 — targeted dependency resolution (review candidate)
Baseline: successful run 45800153144, 21/21 tests, exact upstream sm-action 3.0.1, Rust 1.98.0, signed main de7ce558baa2e63827accb55cf4e65588dcfd721. 269 distinct compiled package entries and 2003 feature-tree lines. No SDK source code or license changes.

## First patch group
| Active dependency | Baseline | Exact resolver target | RustSec |
|---|---|---|---|
| rustls | 0.23.40 | 0.23.46 | 2026-0285,0346,0348,0349 |
| rustls-webpki | 0.103.13 | 0.103.16 | 2026-0382 |
| h2 | 0.4.14 | 0.4.16 | 2026-0258 |
| url | 2.5.8 | 2.5.9 | 2026-0592 |
| crypto-bigint | 0.7.3 | 0.7.6 | 2026-0387 |
| ctutils | 0.4.2 | 0.4.4 | 2026-0385 |
| crossbeam-epoch | 0.9.18 | 0.9.20 | 2026-0204 |

Pinned advisory DB c9f6c91a44dbad9d71742329e9df061279f9c4be. Active version-level matches are not proof of exploitability. The crypto timing issues deserve priority for a secrets integration. No brotli feature observed; quinn-proto and quinn-udp not observed in the Linux graph or compile logs. bytes 1.11.1, cmov 0.5.4, keccak 0.2.0, rand 0.10.1 and time 0.3.47 meet respective reviewed 2026 fix thresholds. Full historic advisory scan remains outstanding. No claim of all advisories resolved.

Separate follow-up: bundled SQLite 0.37.0 requires coordinated rusqlite upgrade or another reviewed supported approach; anyhow 1.0.102 and tokio 1.50.0 are exact root pins and need explicit Cargo.toml revision (candidate 1.0.103 and 1.53.3 respectively); chrono and proc-macro-error2 unmaintained, no direct patched version. Do not add arbitrary SDK changes. Assess dependency constraints and license before further changes.

## Bounded resolution gate
New workflow reuses verified public input acquisition and capture logic, unchanged existing native workflow and original source. One first-attempt dispatch, protected main, owner identity, no token permissions, no credentials, no arbitrary inputs. Network-enabled restricted non-root resolver container only uses Cargo update with fixed exact versions; no build, tests, upstream workflows, executable publication or SDK source modifications. Root manifest remains byte-identical. Only bounded public lock metadata is emitted as base64 plus validated package changes and digest; no artifacts. All non-root packages must retain crates.io origin/checksums; SDK version/checksum unchanged; no more than 80 changed package identities. Indirect version changes are proposals, not automatic acceptance. If constraints fail or expected versions cannot resolve, stop, inspect and choose a separately reviewed correction. No retry of ambiguous dispatch. No production or provider permission. Exact PR review and signed protected merge required before dispatch. Successful resolution is not security clearance or compilation; independently review lock diff and changed packages, then qualify new exact build manifest and run offline tests. Residual online acquisition, shared kernel and bounded VM resource exposure as prior qualification. No independent reviewer or native run result claimed yet.
