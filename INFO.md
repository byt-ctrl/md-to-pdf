# Code Structure and Block-by-Block Explanation: `markdown_to_pdf.py`

This document provides a detailed explanation of each major code block in the `markdown_to_pdf.py` script, describing its purpose and how it works.

---

## 1. Imports
- **Purpose:** Import required Python modules and ReportLab classes for PDF generation and Markdown parsing.
- **Key Imports:**
  - `re`, `os`, `sys`, `argparse`: Standard Python modules for regex, file operations, system functions, and CLI parsing.
  - `reportlab` modules: For PDF creation, styling, and layout.
  - `typing`: For type hints.

---

## 2. MarkdownParser Class
- **Purpose:** Parses Markdown text and converts it into ReportLab elements for PDF rendering.
- **Key Methods:**
  - `__init__`: Initializes the parser, sets up styles.
  - `_setup_custom_styles`: Defines custom styles for headings, code blocks, inline code, and blockquotes.
  - `parse_markdown`: Main method that processes the Markdown text line by line, dispatching to specialized parsers for each Markdown feature.
  - `_parse_header`: Handles Markdown headers (`#`, `##`, etc.), applies heading styles.
  - `_parse_code_block`: Detects and formats code blocks (triple backticks), escapes HTML entities, and applies code style.
  - `_parse_table`: Parses Markdown tables, splits rows/cells, and creates styled ReportLab tables.
  - `_parse_blockquote`: Handles blockquotes (`>`), applies quote style.
  - `_is_list_item`: Utility to check if a line is a list item (ordered or unordered).
  - `_parse_list`: Parses both ordered and unordered lists, supports multi-line items.
  - `_parse_paragraph`: Handles regular text paragraphs, applies inline formatting.
  - `_process_inline_formatting`: Applies inline Markdown formatting (bold, italic, code, links, strikethrough) using regex and ReportLab tags.

---

## 3. MarkdownToPDFConverter Class
- **Purpose:** Orchestrates the conversion process from Markdown to PDF using the parser.
- **Key Methods:**
  - `__init__`: Sets up page size, margins, and initializes the parser.
  - `convert_file`: Reads a Markdown file, parses it, and writes the output PDF.
  - `convert_string`: Converts a Markdown string directly to PDF.
  - `preview_elements`: Returns a preview of parsed elements for debugging (shows type and a snippet of content).

---

## 4. main() Function
- **Purpose:** Provides a command-line interface for the script.
- **Key Steps:**
  - Uses `argparse` to parse CLI arguments (input file, output file, page size, margin, preview mode).
  - Sets up the converter with user-specified options.
  - If `--preview` is set, prints a preview of parsed elements instead of generating a PDF.
  - Otherwise, performs the conversion and prints a success message.
  - Handles errors gracefully and prints them to stderr.

---

## 5. Example Usage Block (if __name__ == "__main__")
- **Purpose:** Provides a self-contained example for testing and demonstration.
- **Key Steps:**
  - If the script is run without CLI arguments, it writes a sample Markdown file (`example.md`) and converts it to PDF (`example.pdf`).
  - Demonstrates all supported Markdown features in the sample.
  - If run with arguments, calls the `main()` function for normal CLI operation.

---

## 6. Comments and Docstrings
- **Purpose:** The code is well-commented and uses docstrings to explain the purpose and usage of classes and methods, aiding readability and maintainability.

---

## Summary Table
| Block/Section                | Purpose/Functionality                                      |
|------------------------------|------------------------------------------------------------|
| Imports                      | Bring in required libraries and modules                    |
| MarkdownParser               | Parse Markdown and convert to ReportLab elements           |
| MarkdownToPDFConverter       | Manage file/string conversion and PDF generation           |
| main()                       | Command-line interface and argument parsing                |
| Example Usage Block          | Demonstration and testing of all features                  |
| Comments & Docstrings        | Documentation and code clarity                             |

---

This structure makes the code modular, easy to extend, and user-friendly for both CLI and programmatic use. For further details, refer to the inline comments and docstrings in the code.
