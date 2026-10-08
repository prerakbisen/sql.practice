# Query Practice

A browser-based SQL interview practice workspace. The question bank is extracted from `300- SQL Queries.pdf`; the document's own numbering repeats and skips numbers, and the extraction yields 332 question entries. The app preserves all entries in the order they appear.

## Run locally

1. Install Node.js 18 or newer.
2. In this directory run `npm install`.
3. Run `npm run dev` and open the local URL printed by Vite.

For a production build, run `npm run build`, then deploy the generated `dist/` folder to any static web host. The SQL engine and its WebAssembly runtime are included in the app, so the database runs locally in your browser without a separate database server or a CDN request.

## Included

- 332 extracted questions with the document's supplied SQL answers where present.
- 36 SQLite sample tables for employees, departments, customers, sales, orders, products, projects, bookings, shipments, and related examples.
- SQL syntax highlighting and a read-only query runner.
- Result comparison against the PDF's supplied answer query on the same sample database. Rows are compared without depending on row order.
- Progress and completion stored in the current browser's local storage.

The PDF provides SQL answer examples, not expected-output tables or a complete canonical data model. Four prompts do not have an extractable answer query; those can still be practiced and manually marked complete. Some PostgreSQL or vendor-specific answer syntax may not run unchanged in the SQLite engine. In those cases the runner still shows results for a valid SQLite query, but cannot provide automatic answer comparison.
