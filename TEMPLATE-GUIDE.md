# TEMPLATE-GUIDE.md — How to Use This Template

> **Delete this file** from your new project once setup is complete.
>
> Each step below shows the **Copilot CLI prompt** to use. Open a terminal, start Copilot CLI, and paste the prompt.

## Quick Start

### Step 1: Create Your New Repository

**Prompt:**
> Create a new private GitHub repo called `<your-repo-name>` from the `darjohn_microsoft/dj-tools-template` template. Clone it to `C:\Users\darjohn\OneDrive - Microsoft\Source\AI projects\<your-repo-name>` and cd into it.

### Step 2: Set Up Azure Storage

**Prompt:**
> Create an Azure resource group called `<rg-name>` in `australiaeast`, then create a storage account called `<storageaccountname>` with Standard_LRS, StorageV2. Enable static website hosting with `index.html` as the index document. Show me the primary endpoint URL when done.

### Step 3: Configure GitHub Repository Variables

**Prompt:**
> Set two GitHub Actions repository variables on this repo: `STORAGE_ACCOUNT` = `<storageaccountname>` and `RESOURCE_GROUP` = `<rg-name>`.

### Step 4: Configure Self-Hosted Runner

**Prompt:**
> Check if the self-hosted runner at `C:\actions-runner` is running. If not, start it.

*(If you don't have a runner yet, set one up via repo Settings → Actions → Runners → New self-hosted runner.)*

### Step 5: Customise the App

**Prompt:**
> This project was created from the dj-tools-template. Customise it for a new app called `<App Name>` that `<describe what the app does>`. Update index.html (title, header, welcome modal, footer, drop zone file types), README.md (name, description, features, hosted URL), docs/SPEC.md, docs/howitworks.md, docs/talktrack.md, and .github/copilot-instructions.md. Replace all placeholder text. Keep the existing Fluent UI theme, dark mode, toast system, and collapsible sections.

### Step 6: Build Features

**Prompt:**
> I want to add `<describe your first feature>`. Update index.html with the implementation. Follow GitHub Flow — create a feature branch, commit, push, and create a PR.

### Step 7: First Deploy

**Prompt:**
> Merge the open PR to main. Check that the GitHub Actions deploy workflow completes, then verify the hosted URL is working.

### Step 8: Clean Up

**Prompt:**
> Delete TEMPLATE-GUIDE.md from this repo, commit and push to main.

---

## What's Included

### Starter `index.html`
- Fluent UI / Microsoft 365 design system (CSS variables)
- Light/dark theme toggle with system detection and localStorage
- Welcome modal with feature overview
- Drag-and-drop file import zone
- Toast notification system
- Collapsible sections with smooth animations
- Keyboard shortcut framework (Ctrl+Z undo, etc.)
- Responsive layout (max-width 1440px)
- Audit log system
- Version display in footer

### CI/CD Workflows
- **`deploy.yml`** — Deploys `index.html` to Azure Blob Storage on push to `main`
- **`validate.yml`** — Validates HTML structure on pull requests

### GitHub Config
- **Issue templates** — Bug report and feature request forms
- **PR template** — Checklist for changes, testing, and documentation
- **Copilot instructions** — Project conventions for AI-assisted development

### Documentation Skeletons
- **`docs/SPEC.md`** — Application specification template
- **`docs/howitworks.md`** — Technical deep-dive template
- **`docs/talktrack.md`** — Demo presentation talk track template

---

## Conventions

| Convention | Details |
|-----------|---------|
| **Architecture** | Single-file HTML, no frameworks, no build step |
| **Git workflow** | GitHub Flow: feature branch → PR → merge to main |
| **Branch naming** | `feature/`, `fix/`, `docs/`, `chore/` prefixes |
| **Versioning** | `v0.0.X-beta` format, bump in footer + README badge |
| **Deployment** | Azure Blob Storage static website via self-hosted runner |
| **Docs** | Update all 4 doc files when features change |
| **OneDrive** | Use `git -c gc.auto=0 push` to avoid gc conflicts |

---

## Checklist

- [ ] Created repo from template
- [ ] Cloned locally
- [ ] Created Azure Storage account
- [ ] Enabled static website hosting
- [ ] Set `STORAGE_ACCOUNT` and `RESOURCE_GROUP` repo variables
- [ ] Self-hosted runner is configured and running
- [ ] Customised `index.html` with app name and features
- [ ] Updated `README.md`
- [ ] Updated `docs/SPEC.md`
- [ ] Updated `.github/copilot-instructions.md`
- [ ] First deploy to main succeeded
- [ ] Verified hosted URL works
- [ ] Deleted this `TEMPLATE-GUIDE.md` file
