# Security and integration contract

This public repository contains a generic, disposable synthetic connectivity test. It does not host a credential broker, private project code, or a general-purpose remote executor.

## Before enabling any credential-bearing run

- Enforce main-branch signed commits, pull-request review, stale-review dismissal, last-push approval, resolved review threads, no force push or deletion, and no ruleset bypass actor.
- Require a separate eligible human reviewer for the synthetic-qualification deployment environment. Prevent self-review and disable administrator bypass in the environment settings. Restrict deployments to main only (no tags or pull requests).
- Enable Actions only after inspecting all workflow files and configuring the approved-action allowlist and full-length SHA pinning. Permit only the reviewed Bitwarden action version. Do not use self-hosted runners, pull_request_target, workflow_run, arbitrary dispatch payloads, or secrets: inherit.
- Confirm all outside-contributor workflow runs require approval and repository default GITHUB_TOKEN permissions are read-only. The qualification job requests no token permissions. Keep secret scanning and push protection enabled where available.
- Use a separate read-only provider identity with access to exactly one disposable synthetic fixture. Do not reuse a development writer token. Confirm provider-enforced effective access and account capacity, not just names or workflow-side UUID checks.
- The test fixture value is the public marker ACCM_SYNTHETIC_CONNECTIVITY_V1. It must not contain real credentials or private data. Configure its UUID using the environment variable setting SYNTHETIC_FIXTURE_UUID, and store the restricted token only as the environment secret SYNTHETIC_BW_ACCESS_TOKEN. Never publish real identifiers or token values. Inspect actual workflow code and the bundled third-party action and dependencies.
- Set the repository variable APPROVED_SHA to the independently accepted merged commit only when ready. Run once from main by the repository owner, then clear the variable and remove/revoke the disposable credential through the provider's supported interface. Concurrency and the first-attempt condition are not a durable one-use ledger. Do not re-run or retry ambiguous results.
- Verify a genuinely successful job and the positive synthetic marker (a skipped job or empty result does not qualify). Verify scope and cleanup separately. Never emit credential values, upload artifacts, enable debug logging, or export secrets to workflow/job outputs or other systems. Public Actions logs must be treated as public even when secrets are masked.

## Cross-project adoption

A reusable workflow runs in the calling repository context; it does not automatically inherit this repository's environment secrets or protection settings. This repository is a source of reviewed patterns, not a shared credential distribution endpoint.

Each adopting repository must separately qualify its own caller identity, operation, provider-side access, execution environment and approval mechanism. Pin reviewed code to immutable versions. No arbitrary commands, target URLs, secret IDs, caller-provided code, public-to-private source checkout, or cross-project credential exports are authorized by this test.

Keep private source and production data in private repositories. A local development session still needs its own supported authentication. A successful synthetic read does not demonstrate write access, project isolation, restart recovery, or permission to perform provider operations in production.

## Residual risk and incident response

Repository administrators can modify settings; protected main is not protection from account takeover. Require strong account authentication, minimal collaborators, and independent review. Provider permissions are the primary credential boundary. On unexpected workflow execution or possible exposure: disable Actions, revoke the affected machine token in the provider, investigate provider and GitHub audit evidence, and requalify before resuming. Public logs, forks and history cannot be assumed erasable.

No real credentials may be attached until all release prerequisites are verified. This contract alone does not approve execution.
