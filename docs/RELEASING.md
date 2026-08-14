# Releasing `finesm`

Releases are managed by Release Please and published to PyPI from the same
GitHub Actions workflow.

## Process

1. Use a Conventional Commit-style pull request title, such as `fix: ...`,
   `feat: ...`, or `feat!: ...`, when squash-merging normal changes.
2. Merging into `master` causes Release Please to open or update a release
   pull request.
3. Review and merge that release pull request. Release Please creates the
   GitHub release and tag, then the workflow tests, builds, and publishes the
   matching distribution to PyPI.

If GitHub marks a release pull request workflow as awaiting approval, a
maintainer must approve it before its checks can run.

## PyPI trusted publishing

The PyPI project must retain this trusted-publisher configuration:

- Repository: `wesleyks/finesm`
- Workflow: `.github/workflows/release-please.yml`
- Environment: none

Publishing uses GitHub Actions OIDC. Do not add, store, or rotate a PyPI API
token for this workflow.

## Verification and guardrails

- Confirm the `publish` job in the Release Please workflow succeeds.
- Confirm the registry version with `python -m pip index versions finesm`.
- Keep GitHub Releases enabled. The publish job runs only after Release Please
  reports that it created a release.
- Do not manually publish or create release tags except for an intentional
  recovery procedure.

