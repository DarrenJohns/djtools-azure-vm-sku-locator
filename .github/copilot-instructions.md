# Copilot Instructions — DJ Tools Web App

## Project Overview
This is a **single-file HTML web application** (`index.html`). It runs as a static site hosted on Azure Blob Storage with no server-side components, build tools, or dependencies.

## Architecture
- **Single file**: All HTML, CSS, and JavaScript live in `index.html`
- **No frameworks**: Pure vanilla HTML/CSS/JS — no React, Vue, npm, etc.
- **No build step**: The file deploys directly to Azure Blob Storage `$web` container
- **Static hosting**: Azure Storage static website

## Git & Deployment Workflow
- **GitHub Flow**: Always create a feature branch → PR → merge to `main`
- **Branch naming**: Use prefixes like `feature/`, `fix/`, `docs/`, `chore/`
- **CI/CD**: Push to `main` triggers `.github/workflows/deploy.yml` which deploys to Azure
- **Validation**: `.github/workflows/validate.yml` runs HTML validation on PRs
- **Self-hosted runner**: GitHub Actions uses a self-hosted runner at `C:\actions-runner` — check it's running before pushing (`Get-Process Runner.Listener`)
- **OneDrive workaround**: Use `git -c gc.auto=0 push` to avoid gc/OneDrive file-locking conflicts

## Version Numbering
- Format: `v0.0.X-beta`
- Update version in: footer in index.html, any generator metadata, README badge
- Bump version for feature changes, not doc-only changes

## Code Conventions
- Keep everything in the single `index.html` file
- Minimal code comments — only where clarification is needed
- CSS uses custom properties (variables) for theming (light/dark mode)
- JavaScript uses modern ES6+ (const/let, arrow functions, template literals, async/await)
- No external CDN dependencies

## Documentation
- `README.md` — Project overview (stays in repo root)
- `docs/SPEC.md` — Full application specification
- `docs/howitworks.md` — Technical deep-dive
- `docs/talktrack.md` — Demo talk track

## Documentation Updates
Any feature added, changed, or removed requires updating these docs before merging:
- `README.md` — Features list, format references, how-to sections
- `docs/SPEC.md` — Full specification
- `docs/howitworks.md` — Technical deep-dive
- `docs/talktrack.md` — Demo talk track (version, recent features)

## Testing
- No automated unit tests — validation is manual + HTML structure validation in CI
- Hard refresh (`Ctrl+Shift+R`) after deployments to bypass browser cache

## Runner Management
- Check the self-hosted runner is running before any push/PR that triggers a workflow
- Ask about shutting down the runner when wrapping up a session
