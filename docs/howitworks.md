# How It Works — [App Name]

> Technical deep-dive into the application architecture and implementation.

## Architecture

This is a **single-file HTML web application** — all HTML, CSS, and JavaScript live in one `index.html` file. There are no frameworks, no build tools, and no external dependencies.

### Why Single-File?
- **Zero setup**: Open the file in any browser
- **Simple deployment**: Upload one file to Azure Blob Storage
- **No dependencies**: Nothing to install, update, or break
- **Portable**: Copy the file anywhere and it works

## File Import

<!-- Describe how your app parses imported files -->

### Supported Formats
- **JSON** — Parsed with `JSON.parse()`, validates structure
- **CSV** — Custom parser handling quoted fields and multi-value cells

### Format Detection
The app detects file format by extension (`.json`, `.csv`).

### Import Flow
1. User drops file onto import zone (or clicks to browse)
2. `FileReader` reads file as text
3. Format-specific parser extracts data
4. Data loaded into application state
5. UI updates to show imported data

## Data Model

<!-- Describe how data is stored in memory -->

```javascript
let appState = {
  name: '',
  items: [],
  warnings: []
};
```

## Editor

<!-- Describe the editing UI and validation -->

### Validation
- Required fields checked before saving
- Duplicate detection
- Range validation for numeric fields

### Undo/Redo
- State snapshots pushed to `undoStack` before each change
- `Ctrl+Z` pops from undo stack, pushes to redo stack
- `Ctrl+Y` pops from redo stack, pushes to undo stack

## Analysis Engine

<!-- Describe any analysis, scoring, or insights -->

## Export System

<!-- Describe each export format and how it's generated -->

### Supported Formats
- **JSON** — `JSON.stringify()` with formatting
- **CSV** — Custom generator with proper escaping

### Export Flow
1. User clicks "Export" button
2. Export modal opens with format tabs
3. Selected format generator produces output
4. User can copy to clipboard or download as file

## Theme System

### CSS Custom Properties
```css
:root {
  --brand-primary: #0f6cbd;
  --bg-base: #fafafa;
  --text-primary: #242424;
  /* ... */
}
```

### Dark Mode
- Toggled via header button
- Overrides CSS custom properties
- Preference saved to `localStorage`
- System preference detected on first visit via `prefers-color-scheme`

## Deployment

### Azure Blob Storage
The app is hosted as a static website on Azure Blob Storage. The `$web` container serves `index.html` at the storage account's static website endpoint.

### CI/CD Pipeline
```
Push to main → GitHub Actions → az storage blob upload → Live
```

The deploy workflow:
1. Checks out the repo
2. Uploads `index.html` to the `$web` container
3. Verifies the deployment with an HTTP request

### HTML Validation
A separate workflow runs on PRs to validate:
- DOCTYPE presence
- Essential HTML tags
- Tag balance (with threshold for JS template strings)
- Common issues (TODO comments, console.log)
