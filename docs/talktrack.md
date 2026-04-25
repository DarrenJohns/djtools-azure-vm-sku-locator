# Talk Track — [App Name] Demo

> Version: v0.0.1-beta
> Duration: ~20 minutes

## Opening (2 min)

**"Today I'll show you [App Name], a tool I built to [solve X problem]. What makes this interesting isn't just the app itself — it's how it was built: entirely with GitHub Copilot CLI, from first line of code to production deployment."**

## The Problem (2 min)

<!-- Describe the problem this app solves -->

## Live Demo (10 min)

### Import
- Show drag-and-drop import
- Point out format auto-detection
- Highlight any warnings or validation

### Edit
- Add/edit/delete items
- Show templates (if applicable)
- Demonstrate undo/redo

### Analyse
- Walk through analysis features
- Show scoring or insights

### Export
- Show multiple format tabs
- Download a file
- Show copy to clipboard

## How It Was Built (4 min)

**"This entire app — the UI, the logic, the CI/CD pipeline, the documentation — was built using GitHub Copilot CLI in my terminal."**

### Key Points
- **Single-file architecture** — One HTML file, no frameworks, no build tools
- **Zero dependencies** — Nothing to install or update
- **AI-assisted development** — Copilot CLI wrote the code, created the repo, set up CI/CD
- **GitHub Flow** — Feature branches, PRs, automated deployment
- **Production in minutes** — From code to live Azure deployment

### Recent Features Built with Copilot
<!-- Update this list as you add features -->
- Initial app scaffold and UI
- File import/export system
- Analysis engine
- CI/CD pipeline setup
- Documentation generation

## Architecture (2 min)

```
index.html → GitHub → Actions → Azure Blob Storage → Live URL
```

- No server, no database, no API
- Self-hosted runner for GitHub Actions
- Azure Storage static website hosting

## Wrap Up (2 min)

**"What started as a simple idea became a production-ready tool in [timeframe]. Copilot CLI handled everything from writing the app to deploying it. The key takeaway: AI-assisted development isn't just about writing code faster — it's about shipping complete solutions."**

### Links
- [GitHub Copilot CLI](https://github.com/features/copilot/cli/)
- [Azure Static Websites](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website)
