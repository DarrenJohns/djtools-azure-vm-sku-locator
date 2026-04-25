# [App Name] — Specification

> Version: v0.0.1-beta

## 1. Overview

<!-- Describe what this application does, who it's for, and the key problem it solves -->

## 2. Architecture

- **Type**: Single-file HTML web application (`index.html`)
- **Frameworks**: None — pure HTML/CSS/JavaScript
- **Dependencies**: Zero external dependencies
- **Hosting**: Azure Blob Storage static website
- **CI/CD**: GitHub Actions → Azure Storage deploy on push to main

## 3. Data Model

<!-- Define the core data structures your app works with -->

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Item name |
| `description` | string | — | Optional description |

## 4. Import

### Supported Formats

<!-- List the file formats your app can import -->

| Format | Extension | Detection |
|--------|-----------|-----------|
| JSON | `.json` | File extension |
| CSV | `.csv` | File extension |

### Import Methods
- Drag and drop onto the import zone
- Click to browse and select a file

## 5. Export

### Supported Formats

<!-- List the file formats your app can export -->

| Format | Extension | Description |
|--------|-----------|-------------|
| JSON | `.json` | Standard JSON output |
| CSV | `.csv` | Spreadsheet-compatible |

## 6. Validation

<!-- Describe validation rules applied to user input -->

## 7. Analysis Engine

<!-- Describe any analysis, scoring, or reporting features -->

## 8. User Interface

### Theme
- Light and dark mode with system detection
- Toggle via header button
- Preference saved to localStorage

### Sections
- Welcome modal (first visit)
- Import zone (drag and drop)
- Editor (main workspace)
- Analysis (insights and scoring)
- Export (multiple format tabs)

## 9. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

## 10. Deployment

- **Hosting**: Azure Blob Storage `$web` container
- **CI/CD**: GitHub Actions workflow on push to `main`
- **Runner**: Self-hosted runner at `C:\actions-runner`
