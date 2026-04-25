# 🛡️ [App Name]

<!-- TODO: Once CI/CD is configured, replace the static deploy badge below with a live one:
[![Deploy](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/deploy.yml/badge.svg)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/deploy.yml)
-->
![Deploy](https://img.shields.io/badge/deploy-not_configured-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue)
![Azure](https://img.shields.io/badge/Azure-Tool-0078D4)
![Version](https://img.shields.io/badge/version-0.0.1--beta-orange)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

> **[One-line description of what this app does]**

<!-- TODO: Replace with your Azure Static Website URL -->
🌐 **[Live App](https://YOUR_STORAGE_ACCOUNT.z8.web.core.windows.net/)**

---

## ✨ Features

<!-- TODO: Update this table with your app's actual features -->

| Category | Features |
|----------|----------|
| **Import** | Drag-and-drop file import |
| **Edit** | Add, modify, duplicate, delete items |
| **Analyse** | Real-time analysis and validation |
| **Export** | Multiple output formats |
| **Tools** | Built-in calculators and reference data |

## 🚀 Getting Started

This is a single-file HTML web application — no installation, build tools, or dependencies required.

### Hosted Version

<!-- TODO: Replace with your actual hosted URL, or remove if not hosted yet -->

Visit the live app at: **[your hosted URL]**

### Run Locally

Open `index.html` directly in any modern browser — the app works entirely client-side.

### How to Use

<!-- TODO: Replace these steps with your app's specific workflow -->

1. **Import** — Drag and drop a file or start from scratch
2. **Edit** — Use the editor to add and modify items
3. **Analyse** — Review the analysis and scoring
4. **Export** — Download in your preferred format

## 🏗️ Architecture

| Aspect | Details |
|--------|---------|
| **Type** | Single-file HTML web application |
| **Frameworks** | None — pure HTML/CSS/JS |
| **Dependencies** | Zero |
| **Build step** | None — file deploys directly |
| **Hosting** | Azure Blob Storage static website |
| **CI/CD** | GitHub Actions with self-hosted runner |

## 📁 Project Structure

```
├── index.html                          # The entire application
├── README.md                           # This file
├── TEMPLATE-GUIDE.md                   # Setup guide (delete after setup)
├── docs/
│   ├── SPEC.md                         # Application specification
│   ├── howitworks.md                   # Technical deep-dive
│   └── talktrack.md                    # Demo talk track
└── .github/
    ├── copilot-instructions.md         # AI assistant conventions
    ├── pull_request_template.md        # PR checklist
    ├── workflows/
    │   ├── deploy.yml                  # Deploy to Azure on push to main
    │   └── validate.yml                # HTML validation on PRs
    └── ISSUE_TEMPLATE/
        ├── bug_report.yml
        └── feature_request.yml
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [SPEC.md](docs/SPEC.md) | Full application specification |
| [How It Works](docs/howitworks.md) | Technical deep-dive |
| [Talk Track](docs/talktrack.md) | Demo presentation notes |
| [Template Guide](TEMPLATE-GUIDE.md) | How to set up from this template |

## 🛠️ Development

This app follows **GitHub Flow**:

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes to `index.html`
3. Push and create a PR
4. Merge to `main` → auto-deploys to Azure

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>DJ Tools</strong> powered by <a href="https://github.com/features/copilot/cli/">GitHub Copilot CLI</a>
</div>
