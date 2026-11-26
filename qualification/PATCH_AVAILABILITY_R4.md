# R4 — registry availability correction, bounded new resolution
Prior run 45805697118, workflow431493735 run1/attempt1, failed closed on yanked target during acquisition; consumed, no retry. Prior R3 signed main df5e757b1f0ad98a4b0ab6879f1c3e757b3f38c1, successful baseline run45800153144 unchanged (21/21). New workflow path only; original one-shot workflow and all security rules unchanged.

## Verified index snapshot
Official rust-lang/crates.io-index commit 1550b7e089a3c3e864f1cf50cce3e928554bce09, 2026-11-26T11:00:41Z. All eight proposed exact rows non-yanked and Rust MSRV <=1.87 (pinned Rust1.98.0). SHA256 values below are registry archive checksums, not proof of retrieved archives; actual acquisition must match.
| Package | Exact target | SHA256 |
|---|---|---|
| rustls | 0.23.46 | 48e13bd8c0e9365c43cfa5c9e8f9ad49d3c8444926c9aac819e0e4dc503c8fdf |
| rustls-webpki | 0.103.16 | 4443b1b6d39d7c663139942cc4558262562d2c84123bb6282ef177009ca8b281 |
| h2 | 0.4.16 | a9f37a958b41b3b19ee2707c06439c0e9e547e847223eb791ecb0cb821c65e27 |
| url | 2.5.9 | f00cd2407bb42c0ef17be88d4cf020f5cceffd121665bac9b8b9493a369b3b1a |
| crypto-bigint | 0.7.9 | d811ea23fdfbcce2e2d5132344d471abdb8f901ac496a0893a3df92e70525e52 |
| ctutils | 0.4.5 | 38d28fb6aa7dd680b3ffd1a3e64e115c177bdba63c0ae7f9cd48129ff05c4fa0 |
| crossbeam-epoch | 0.9.20 | 2d6914041f254d6e9176c01941b21115dcfb7089e55135a35411081bd106ef3f |
| form_urlencoded | 1.2.3 | afa489199eaffb1211795df1c6236ce1ad0d41a6fa45250add73e3b02420f06e |

crypto-bigint 0.7.6/0.7.7/0.7.8 yanked. First non-yanked 0.7.9 meets RUSTSEC-2026-0387 patched floor; ctutils 0.4.5 meets RUSTSEC-2026-0385 floor and crypto-bigint ^0.4.5 requirement. Upstream changelog https://docs.rs/crate/crypto-bigint/0.7.9/source/CHANGELOG.md reports compatibility-impacting Mul change in 0.7.9; actual compilation/regression mandatory, no assurance from version constraint alone. URL2.5.9 needs form_urlencoded ^1.2.3, baseline1.2.2; add exact support update. crypto-bigint 0.7.9 optional der/hybrid-array requires ^0.4.12 only if enabled; actual baseline graph 2003 lines shows rand_core, alloc, zeroize, not der. Original crypto-bigint lock edges also exclude der/hybrid-array. Keep hybrid-array0.4.10 and typenum1.19.0 because hybrid-array0.4.12 requires typenum^1.20 and bitwarden-crypto3.0.0 explicitly requires >=1.18,<1.20. Do not broaden those updates or modify SDK. Registry metadata for RSA0.10.0-rc.18 and crypto-primes0.7.1 permits ^0.7, but runtime behavior/API compatibility unverified. Direct requirement assessment is not a full transitive/target-feature solve; finite registry may still fail on unavailable versions or incompatible graph. Pinned RustSec DB c9f6c91a44dbad9d71742329e9df061279f9c4be has no advisory entries for form_urlencoded, hybrid-array, typenum; no comprehensive vulnerability clearance claimed.

## Scope and admission
Reuse exact R3 containment with new path and workflow name, 387 baseline archives + 8 approved target archives =395, explicit target checksums and fail-closed live non-yanked check with precise package/version diagnostic, support dependencies ordered before parents. All prior nonroot/offline containers, bounded stream and graph/full frozen metadata verification remain. Actual target checksums and yanked status rechecked at runtime; availability can change. New run1/attempt1 only after fresh technical review and eligible approval, signed exact protected merge, zero secrets/variables and new workflow history empty. No retry of old run. No provider, credentials, build, release or production admission. No native result yet.
