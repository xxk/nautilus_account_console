# GitHub Project Skeleton Acceptance / GitHub 项目骨架验收

- Date: 2026-06-13
- Project: `nautilus_account_console`
- Scope: GitHub-ready repository architecture
- Verdict: accepted as local GitHub-ready skeleton, remote repository not yet created

## 1. Acceptance Summary

| Area | Status | Evidence |
| --- | --- | --- |
| Local git repository | pass | `git init -b main` completed |
| GitHub Actions CI | pass | `.github/workflows/ci.yml` exists |
| Python CI job | pass | installs backend, compiles Python, runs backend tests |
| Rust CI job | pass | runs `cargo test --manifest-path hotpath-rs/Cargo.toml` |
| Frontend CI job | pass | uses Node 22, runs `npm install` and `npm run build` in `frontend/` |
| Boundary scan job | pass | scans implementation paths for forbidden readiness/runtime wording |
| PR template | pass | `.github/pull_request_template.md` exists with validation and boundary checklist |
| Issue templates | pass | feature and bug issue forms exist |
| Dependabot | pass | configured for backend pip, Rust cargo and frontend npm |
| CODEOWNERS | partial | placeholder file exists; real GitHub owner/team names are still needed |
| GitHub architecture doc | pass | `docs/architecture/github-project-architecture.md` exists |
| Remote repository | not yet | owner/name not provided; no remote configured |

## 2. Local Validation

Executed on 2026-06-13:

```powershell
python -m pytest backend\tests
cargo test --manifest-path hotpath-rs\Cargo.toml
rg -n "Paper ready|Live ready|admitted|production ready|capital allocated|can trade|place order|latest/|debug/|raw report.*truth|runtime truth|capital truth|submit order|cancel order|replace order" frontend\src backend\src hotpath-rs\crates
```

Observed results:

```text
pytest: 2 passed
cargo test: 3 passed
implementation boundary scan: no matches
```

## 3. Explicit Non-Acceptance

This acceptance does not claim:

1. Remote GitHub repository exists.
2. Branch protection is configured.
3. GitHub teams/users are wired into CODEOWNERS.
4. GitHub Actions has run on GitHub infrastructure.
5. Frontend build has been verified locally, because local Node/npm is unavailable in the current environment.

## 4. Remote Publish Checklist

When the GitHub owner/name is known:

```powershell
git add .
git commit -m "Bootstrap Nautilus Account Console MVP skeleton"
git remote add origin https://github.com/<owner>/nautilus_account_console.git
git push -u origin main
```

After push:

1. Enable branch protection for `main`.
2. Require the four CI jobs from `.github/workflows/ci.yml`.
3. Replace `.github/CODEOWNERS` placeholders with real users or teams.
4. Confirm GitHub Actions passes on the first PR.
5. Add repository description: `Read-only event-driven account console for Nautilus read models`.

