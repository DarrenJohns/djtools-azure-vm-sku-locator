# Copilot Instructions — VM SKU Per Region

## Project Overview
This is a **single-file HTML web application** (`index.html`) with pre-fetched static JSON data. It shows Azure VM SKU availability per region, helping VM administrators understand what virtual machine sizes are available. No user authentication required.

## Architecture
- **Single file**: All HTML, CSS, and JavaScript live in `index.html`
- **Data files**: Pre-fetched JSON in `data/` directory (one file per region, plus `regions.json`, `metadata.json`, `retirements.json`, and `data/history/` for archived snapshots)
- **Configuration**: `config.json` defines target regions for data refresh
- **Scripts**: `scripts/normalize-skus.py` (normalizer) and `scripts/update-retirements.py` (retirement scraper)
- **No frameworks**: Pure vanilla HTML/CSS/JS — no React, Vue, npm, etc.
- **No build step**: The file deploys directly to Azure Blob Storage `$web` container
- **No authentication**: Data is pre-fetched monthly, no user login needed
- **Static hosting**: Azure Storage static website

## Data Pipeline
- SKU data is fetched monthly via `az vm list-skus` for each region
- Regions to refresh are configured in `config.json`
- Raw data is normalized to a consistent JSON schema via `scripts/normalize-skus.py` (extracting capabilities into flat fields)
- Previous data is archived to `data/history/` before each refresh (enables the What's New feature)
- Retirement data is refreshed via `scripts/update-retirements.py` which writes `data/retirements.json`
- Combined workflow: `.github/workflows/refresh-vm-skus.yml` handles SKU fetch + normalization + retirement refresh + history archiving
- Key fields: name, family, vCPUs, memoryGB, cpuArchitecture, zones, acceleratedNetworking, premiumIO, ephemeralOSDisk, spotEligible, etc.
- Family names are mapped to user-friendly display names and Azure docs URLs (best-effort)

## Git & Deployment Workflow
- **GitHub Flow**: Always create a feature branch → PR → merge to `main`
- **Branch naming**: Use prefixes like `feature/`, `fix/`, `docs/`, `chore/`
- **CI/CD**: Push to `main` triggers `.github/workflows/deploy.yml` which deploys to Azure
- **Validation**: `.github/workflows/validate.yml` runs HTML validation on PRs
- **SKU refresh**: `.github/workflows/refresh-vm-skus.yml` runs monthly SKU fetch + normalization + retirement refresh + history archiving
- **Self-hosted runner**: GitHub Actions uses a self-hosted runner at `C:\actions-runner-vmsku`
- **OneDrive workaround**: Use `git -c gc.auto=0 push` to avoid gc/OneDrive file-locking conflicts

## Version Numbering
- Format: `v0.0.X-beta`
- Update version in: footer in index.html, README badge
- Bump version for feature changes, not doc-only changes

## Code Conventions
- Keep application logic in the single `index.html` file
- Data files live in `data/` directory
- Minimal code comments — only where clarification is needed
- CSS uses custom properties (variables) for theming (light/dark mode)
- JavaScript uses modern ES6+ (const/let, arrow functions, template literals, async/await)
- No external CDN dependencies
- Family-to-docs URL mapping is best-effort — always provide a fallback link
- **Collapsible sections**: Use the `collapsed` CSS class on section bodies to collapse sections. NEVER use inline `display:none` on section bodies.
- **overflow:hidden restriction**: Do NOT add `overflow:hidden` to `.section` elements — it clips rotated column headers in tables.
- Scripts (`scripts/`) are Python — keep them simple and self-contained
- `config.json` is the single source of truth for which regions to refresh

## Documentation
- `README.md` — Project overview (stays in repo root)
- `docs/SPEC.md` — Full application specification
- `docs/howitworks.md` — Technical deep-dive
- `docs/talktrack.md` — Demo talk track

## Documentation Updates
Any feature added, changed, or removed requires updating these docs before merging:
- `README.md` — Features list, how-to sections
- `docs/SPEC.md` — Full specification
- `docs/howitworks.md` — Technical deep-dive
- `docs/talktrack.md` — Demo talk track (version, recent features)

## Retirement System
- `data/retirements.json` contains VM family retirement data (family name, dates, replacement)
- `scripts/update-retirements.py` scrapes Azure retirement announcements
- SKUs from retiring families show ⚠️ badges in the UI
- Retirement data is refreshed as part of the monthly `refresh-vm-skus.yml` workflow

## History & Archiving
- Previous SKU data is archived to `data/history/` before each monthly refresh
- The What's New section in the UI compares current data with the previous snapshot
- Shows SKUs added and removed since last refresh
- `data/history/.gitkeep` ensures the directory exists in git

## Testing
- No automated unit tests — validation is manual + HTML structure validation in CI
- Hard refresh (`Ctrl+Shift+R`) after deployments to bypass browser cache
- Test with at least one region to verify data loading, filtering, sorting, and export

## Runner Management
- Check the self-hosted runner is running before any push/PR that triggers a workflow
- Ask about shutting down the runner when wrapping up a session
