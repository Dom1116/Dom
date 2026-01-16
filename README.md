# ReceiptWise Static Site

A modern, single-page landing site for ReceiptWise with privacy and terms placeholders.

## Project Structure

```
.
├── assets/
│   └── logo.svg
├── index.html
├── privacy.html
├── terms.html
└── README.md
```

## Preview Locally

### Option 1: Open directly

Open `index.html` directly in your browser.

### Option 2: Python simple server

```bash
python3 -m http.server 5173
```

Then open:

```
http://localhost:5173
```

### Option 3: Node static server (optional)

```bash
npx serve .
```

Then open the URL printed in the terminal.

## Deploy

### Netlify Drop

1. Go to [https://app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag and drop the entire project folder.
3. Netlify will provide a live URL instantly.

### GitHub Pages

1. Create a GitHub repository and push this project.
2. In GitHub, go to **Settings → Pages**.
3. Under **Source**, choose your default branch and **/root**.
4. Save and wait for the deployed URL to appear.
