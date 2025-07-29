# Markdown to PDF Converter

A Python-based tool that converts Markdown files to professionally formatted PDF documents using ReportLab.

## Features

- Comprehensive Markdown support including:
  - Headers (H1-H6)
  - Bold and italic text
  - Code blocks with syntax highlighting
  - Tables with formatting
  - Blockquotes
  - Ordered and unordered lists
  - Horizontal rules
  - Inline formatting (bold, italic, code, links, strikethrough)
- Customizable page sizes (Letter, A4)
- Adjustable margins
- Preview mode for debugging
- Clean command-line interface

## Installation

1. Ensure you have Python 3.x installed
2. Install required dependencies:
```bash
pip install reportlab
```

## Usage

### Command Line Interface

Basic usage:
```bash
python markdown_to_pdf.py input.md -o output.pdf
```

Options:
- `-o`, `--output`: Specify output PDF file name
- `-p`, `--page-size`: Choose page size ('letter' or 'a4')
- `-m`, `--margin`: Set page margin in inches (default: 0.75)
- `--preview`: Preview parsed elements without generating PDF

Examples:
```bash
# Convert with default settings
python markdown_to_pdf.py document.md

# Specify output file
python markdown_to_pdf.py document.md -o result.pdf

# Use A4 paper size with 1-inch margins
python markdown_to_pdf.py document.md -p a4 -m 1.0

# Preview parsed elements
python markdown_to_pdf.py document.md --preview
```

### Python API

```python
from markdown_to_pdf import MarkdownToPDFConverter

# Create converter instance
converter = MarkdownToPDFConverter()

# Convert file
converter.convert_file('input.md', 'output.pdf')

# Or convert string directly
markdown_content = "# Title\nThis is **bold** text."
converter.convert_string(markdown_content, 'output.pdf')
```

## Supported Markdown Syntax

- Headers:
  ```markdown
  # H1 Header
  ## H2 Header
  ### H3 Header
  ```

- Emphasis:
  ```markdown
  **bold text** or __bold text__
  *italic text* or _italic text_
  ~~strikethrough text~~
  ```

- Code:
  ````markdown
  `inline code`
  ```python
  def code_block():
      return True
  ```
  ````

- Lists:
  ```markdown
  - Unordered item
  * Another item
  + Yet another item

  1. Ordered item
  2. Second item
  3. Third item
  ```

- Tables:
  ```markdown
  | Header 1 | Header 2 |
  |----------|----------|
  | Cell 1   | Cell 2   |
  ```

- Blockquotes:
  ```markdown
  > This is a blockquote
  > It can span multiple lines
  ```

- Links:
  ```markdown
  [Link text](https://example.com)
  ```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.
