# Test, promote and roll back releases

Promote a tested image through environments and rehearse a rollback. Carry the same application policies and evaluation criteria into each stage.

**Supporting · 60 minutes** · **Prerequisites** [Describe infrastructure with Terraform](terraform.md) and [Package the API with Docker](../06-azure/containers.md).

## The problem

A new image can pass readiness and still answer policy questions incorrectly. A release needs application checks, AI quality checks, a reproducible artifact, and a way to restore traffic.

## Read a delivery workflow

This GitHub Actions step excerpt assumes the repository has been checked out, Python selected, and tutorial dependencies installed inside the job.


```yaml
steps:
  - name: Check the handbook
    run: python -m mkdocs build --strict
  - name: Print retrieval benchmark evidence
    run: python -m examples.evaluation
```


The second step prints evidence. It needs assertions or an explicit threshold gate to block a release. Add separate checks for tenant isolation and write approval. Do not rely on an average quality score to detect a security regression.

## Trace a release

1. On a pull request, run tests, compare evaluation results and review config changes.
2. After merge, build an image, publish it, and record its digest with prompt, model, and dataset versions.
3. Deploy that digest to staging. Check readiness, authentication, citations, and stream completion.
4. Promote the identical digest to production behind an environment approval when required. Start with a small traffic share in Container Apps multiple-revision mode and compare error and quality signals.
5. Move traffic back to the previous healthy revision when the release breaches the agreed gate. Capture the revision IDs and the reason.

GitHub's OIDC token can be exchanged for a short-lived Azure credential by a trusted deployment job. Restrict federation to the expected repository and environment claims. Give PR jobs read-only permissions, and restrict `id-token: write` and Azure deployment permissions to the release job.

## Practice and debugging

Revision B passes health checks. The sample question starts citing an older policy after promotion. Switch traffic back to A, then check if A can read the current schema and corpus. Expect returning traffic to recover the previous behavior only if those dependencies are compatible. A migration that dropped an old column may require a forward fix or data recovery instead.

## In production

Use additive schema changes first and remove old fields after existing revisions no longer need them. Treat model and prompt settings as part of the release. A rollback should restore compatible inputs and state as well as code. Document whether each setting is revision-scoped or shared across revisions.

## Recap and next step

You can separate artifact promotion, traffic management, and data compatibility. [Next: Observe quality, latency and cost](../08-production-ai/observability.md)

[GitHub Actions OIDC in Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure), [Container Apps revisions](https://learn.microsoft.com/en-us/azure/container-apps/revisions)
