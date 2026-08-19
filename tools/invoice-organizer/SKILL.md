---
name: invoice-organizer
description: |
  "Expert classification, metadata extraction, standardized renaming, and structural archiving of financial invoices and receipts. Trigger this skill when asked to organize, rename, catalog, parse, or prepare invoices, receipts, bills, and payment records for accounting or tax purposes. Keywords: invoice, receipt, tax prep, PDF parsing, OCR, vendor name, expense category, invoice-summary.csv, YYYY-MM-DD."

  "Expert classification, metadata extraction, standardized renaming, and structural archiving of financial invoices and receipts. Trigger this skill when asked to organize, rename, catalog, parse, or prepare invoices, receipts, bills, and payment records for accounting or tax purposes. Keywords: invoice, receipt, tax prep, PDF parsing, OCR, vendor name, expense category, invoice-summary.csv, YYYY-MM-DD."

---

# Invoice & Receipt Organizer

This is a self-contained skill. Do NOT load external files or reference directories.

## Mindset & Philosophy
Accurate accounting requires precision. When organizing financial documents, a single digit error in a date or amount can cause tax discrepancies or reconciliation failures. Treat filenames as structured database records. Prioritize consistency, metadata cleanliness (stripping tracking info), and programmatic verification.

---

## Processing Decision Tree

```mermaid
graph TD
    A[Identify Document Format] --> B{Is it a PDF or Image?}
    B -->|PDF| C{Is text selectable?}
    B -->|Image| D[Run CLI OCR or Python Tesseract/Pillow extraction]
    
    C -->|Yes| E[Programmatic text extraction via PyMuPDF / pdftotext]
    C -->|No| D
    
    E --> F[Extract Date, Vendor, Amount, Invoice ID]
    D --> F
    
    F --> G{Is date format ambiguous?}
    G -->|Yes (e.g. 05/06/2024)| H[Analyze vendor origin & layout to resolve MM/DD vs DD/MM]
    G -->|No| I[Standardize to YYYY-MM-DD]
    H --> I
    
    I --> J[Standardize filename & copy to directory structure]
```

### Extraction Options & Strategy

| Document Type | Primary Method | Fallback Method | Key Target Metadata |
| :--- | :--- | :--- | :--- |
| Selecetable PDF | Python (`pypdf` or `pymupdf` script) | CLI `pdftotext` | Exact string match for "Total Due", "Grand Total", "Date of Issue" |
| Scanned Image / PDF | OCR tool (`tesseract`) | LLM visual verification | High-contrast preprocessing (binarize image first for cleaner OCR) |
| HTML Receipt | Python `BeautifulSoup` | Pandoc to markdown | Locate CSS selectors or markdown tables for line-items |

---

## Domain-Specific Procedures

### 1. Ambiguous Date Resolution
Different countries use conflicting formats. If you see `03-04-2024`:
* Look up the vendor headquarters: If US-based, default to `2024-03-04` (March 4). If EU/UK-based, default to `2024-04-03` (April 3).
* Check the rest of the document for helper strings (e.g. "Payment due by April 3rd").
* If unresolved, use the file modification metadata as a reference checkpoint, but append a `-REVIEW-DATE` flag to the filename.

### 2. Standardized Naming Convention
Every file must be renamed to:
`YYYY-MM-DD <Vendor Name> - Invoice <Invoice ID> - <Description>.<extension>`
* Clean all vendor names: Remove legal suffixes like `LLC`, `Inc.`, `Corp`, or `GmbH`.
* Remove all non-alphanumeric characters from description (except hyphens and spaces).
* Example: `2026-07-15 Stripe - Invoice INV-984712 - Monthly Payment Processing.pdf`

### 3. Archive Directory Layout
Sort documents into a nested hierarchy based on the target audience (Accountant vs Internal Tracker):

```
Invoices/
├── 2026/
│   ├── Q3/
│   │   ├── Software/
│   │   │   ├── 2026-07-15 Stripe - Invoice INV-984712.pdf
│   │   │   └── 2026-07-16 AWS - Invoice 1092847.pdf
│   │   └── Travel/
│   └── Q4/
└── invoice-summary.csv
```

---

## NEVER Anti-Patterns

| Action | Why | Consequences | Correct Alternative |
| :--- | :--- | :--- | :--- |
| **NEVER** move (`mv`) original files directly without preserving a backup folder or copying (`cp`). | If parsing logic fails mid-run, original unorganized files may be lost or corrupted. | Hard data loss, unrecoverable invoices. | Always copy (`cp`) files to the new structure, verifying integrity before deleting source files. |
| **NEVER** assume the first date in a document is the invoice date. | Documents contain multiple dates: period start/end, due date, payment date, and transaction date. | Incorrect sorting, tax period misalignment. | Verify the date label (e.g., "Invoice Date", "Bill Date") instead of matching the first regex pattern. |
| **NEVER** overwrite existing files when duplicates are detected. | Two invoices can share the same date and vendor (e.g., separate purchases on the same day). | One of the invoices gets deleted/overwritten. | Append a numeric suffix (e.g., `_1`, `_2`) if vendor and date are identical. |
| **NEVER** ignore tax deductibility tags if visible on the receipt. | Accountants require segregation of tax-deductible business expenses vs personal/non-deductible items. | Increased accounting overhead, audited tax filings. | Add a tag to the CSV output (e.g. `Deductible=True`) and place in corresponding folder. |

---

## Freedom Calibration
* **Low Freedom (Strict Rules):** The naming format (`YYYY-MM-DD Vendor - Invoice ID - Description`) and CSV column sequence must remain completely invariant to ensure programmatic ingestion works.
* **Medium Freedom (Operational):** Folder sorting structure (by Vendor vs by Category) can be adjusted to match client requirements or accountant feedback.

---

## Error Handling & Fallbacks

### 1. PDF Has No Selectable Text (Scanned Document)
* **Fallback**: Run `tesseract` or Python OCR packages to read the file. If OCR is unavailable, use visual verification features if available in the model environment. If visual assessment is not possible, name the file `YYYY-MM-DD-UNPARSED-Vendor-Invoice.pdf` based on filename hints and put it in a `needs-manual-review/` subdirectory.

### 2. CSV Summary Write Failures
* **Failure**: Disk write permission block or lock on CSV file.
* **Fallback**: Write a temporary JSON summary file (`.invoice-temp.json`) in the same directory, complete the renaming/moving operations, then attempt to convert JSON to CSV. Print the raw CSV rows directly to the terminal output so the user has a copy of the data.


## 6) Memory Sync

After completing a task, key decision, or report, you **MUST** trigger the local memory capture. 

1. Save the final document, report, or summary as a Markdown file in the project directory.
2. Invoke the capture script: 
   `ash
   python \capture_knowledge.py <file_path>
   `
3. This ensures that new requirements, technical standards, and findings are automatically routed to the correct storage (OKF or ChromaDB).
