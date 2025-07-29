import re
import os
import sys
import argparse
from reportlab.lib import colors
from reportlab.lib.units import inch
from typing import List,Tuple,Dict,Any
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.colors import black,blue,red,green
from reportlab.platypus import PageBreak,Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER,TA_RIGHT,TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle

# markdown_to_pdf.py
# This script converts markdown files to PDF using reportlab.
# It supports headers , code blocks , tables , blockquotes , lists , and inline formatting.


class MarkdownParser :
    """MarkdownParser class to convert markdown text to reportlab elements. """

    """
    a comprehensive markdown parser that handles various markdown elements.
    It supports headers, code blocks, tables, blockquotes, lists, horizontal rules,
    and inline formatting such as bold , italic , links , and strikethrough etc .
    """
    
    def __init__(self) :
        self.elements=[]
        self.styles=getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self) :
        """setup custom styles for different markdown elements."""
        # heading styles
        for a in range(1,7) :
            style_name=f'Heading{a}'
            if style_name not in self.styles :
                size=18-(a*2)
                self.styles.add(ParagraphStyle(
                    name=style_name,
                    parent=self.styles['Heading1'],
                    fontSize=max(size,10),
                    spaceAfter=12,
                    spaceBefore=12,
                    textColor=black
                ))
        
        # code block style
        self.styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=9,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12,
            spaceBefore=12,
            backColor=colors.lightgrey,
            borderColor=colors.grey,
            borderWidth=1,
            borderPadding=10
        ))
        
        # inline code style
        self.styles.add(ParagraphStyle(
            name='InlineCode',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=10,
            backColor=colors.lightgrey
        ))
        
        # quote style
        self.styles.add(ParagraphStyle(
            name='Quote',
            parent=self.styles['Normal'],
            leftIndent=30,
            rightIndent=30,
            fontName='Times-Italic',
            fontSize=11,
            textColor=colors.grey,
            borderColor=colors.blue,
            borderWidth=2,
            borderPadding=10,
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def parse_markdown(self,markdown_text : str) -> List[Any] :
        """parse markdown text and return a list of reportlab elements."""
        lines=markdown_text.split('\n')
        a=0

        while a<len(lines):
            line=lines[a].rstrip()

            # skip empty lines
            if not line :
                a+=1
                continue
            
            # headers
            if line.startswith('#') :
                a=self._parse_header(line,a)

            # code blocks
            elif line.startswith('```'):
                a=self._parse_code_block(lines,a)

            # tables
            elif '|' in line and a + 1 < len(lines) and '---' in lines[a + 1]:
                a=self._parse_table(lines,a)

            # blockquotes
            elif line.startswith('>'):
                a=self._parse_blockquote(lines,a)

            # lists
            elif self._is_list_item(line):
                a=self._parse_list(lines,a)

            # horizontal rule
            elif re.match(r'^[-*_]{3,}$', line.strip()):
                self.elements.append(Spacer(1,0.2*inch))
                a+=1

            # Regular paragraph
            else:
                a=self._parse_paragraph(lines,a)

        return self.elements
    

    def _parse_header(self,line : str,index : int)->int :
        
        """parse markdown headers."""
        match=re.match(r'^(#{1,6})\s+(.+)', line)
        if match :
            level=len(match.group(1))
            text=match.group(2)
            style_name=f'Heading{level}'

            # process inline formatting
            formatted_text=self._process_inline_formatting(text)
            
            self.elements.append(Paragraph(formatted_text,self.styles[style_name]))
            self.elements.append(Spacer(1,0.1*inch))
        
        return index+1
    
    def _parse_code_block(self, lines : List[str] , index : int)->int :
        """parse code blocks."""
        a=index+1
        code_lines=[]
        language=lines[index][3:].strip()  # get's language if specified
        
        while a<len(lines) and not lines[a].startswith('```') :
            code_lines.append(lines[a])
            a+=1

        if code_lines :
            code_text='\n'.join(code_lines)
            # escape HTML entities for reportlab
            code_text=code_text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            self.elements.append(Paragraph(f'<pre>{code_text}</pre>',self.styles['CodeBlock']))
            self.elements.append(Spacer(1,0.1*inch))
        
        return a+1 if a<len(lines) else len(lines)
    
    def _parse_table(self,lines : List[str],index : int) -> int :
        """parse markdown tables."""
        table_lines=[]
        a=index
        
        # collect table lines
        while a<len(lines) and '|' in lines[a] :
            if not re.match(r'^\s*\|[\s\-:]*\|\s*$',lines[a]):  # skip separator lines
                table_lines.append(lines[a])
            a+=1
        
        if len(table_lines)>1 :  # at least header + one row
            table_data=[]
            for line in table_lines :
                # split by | and clean up
                cells=[cell.strip() for cell in line.split('|')[1:-1]]
                if cells:  # skip empty rows
                    table_data.append(cells)
            
            if table_data :
                # create table
                table=Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND',(0,0), (-1, 0),colors.grey),
                    ('TEXTCOLOR',(0,0), (-1, 0),colors.whitesmoke),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                    ('FONTSIZE',(0,0),(-1,0),12),
                    ('BOTTOMPADDING',(0,0),(-1,0),12),
                    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
                    ('GRID',(0,0),(-1,-1),1,colors.black)
                ]))
                
                self.elements.append(table)
                self.elements.append(Spacer(1,0.2*inch))
        
        return a
    
    def _parse_blockquote(self, lines : List[str] , index : int) -> int :
        """parse blockquotes."""
        quote_lines=[]
        a=index

        while a<len(lines) and lines[a].startswith('>') :
            quote_text=lines[a][1:].strip()
            if quote_text :
                quote_lines.append(quote_text)
            a+=1
        
        if quote_lines : 
            quote_text=' '.join(quote_lines)
            formatted_quote=self._process_inline_formatting(quote_text)
            self.elements.append(Paragraph(formatted_quote,self.styles['Quote']))
            self.elements.append(Spacer(1,0.1*inch))

        return a
    
    def _is_list_item(self,line : str) -> bool :
        """check if line is a list item."""
        return bool(re.match(r'^\s*[-*+]\s+',line) or re.match(r'^\s*\d+\.\s+',line))

    def _parse_list(self,lines : List[str], index : int) -> int :
        """parse markdown lists."""
        list_items=[]
        a=index

        while a<len(lines) and (self._is_list_item(lines[a]) or lines[a].startswith('  ')):
            line=lines[a]
            if self._is_list_item(line) :
                # extract's list item content
                # characters is taken from online like • etc 
                if re.match(r'^\s*[-*+]\s+', line):
                    content=re.sub(r'^\s*[-*+]\s+','',line)
                    list_items.append(f"• {content}")
                elif re.match(r'^\s*\d+\.\s+', line):
                    content=re.sub(r'^\s*\d+\.\s+','',line)
                    list_items.append(f"{len(list_items)+1}. {content}")
            else :
                # continuation of previous list item
                if list_items :
                    list_items[-1]+=f" {line.strip()}"
            a+=1
        
        # create paragraphs for each list item
        for item in list_items :
            formatted_item=self._process_inline_formatting(item)
            self.elements.append(Paragraph(formatted_item, self.styles['Normal']))

        if list_items :
            self.elements.append(Spacer(1,0.1*inch))
        
        return a
    
    def _parse_paragraph(self,lines : List[str],index : int)->int :
        """parse regular paragraphs."""
        paragraph_lines=[]
        a=index
        
        # collect lines until empty line or special formatting
        while a<len(lines) and lines[a].strip() :
            if (lines[a].startswith('#') or lines[a].startswith('```') or 
                lines[a].startswith('>') or self._is_list_item(lines[a]) or
                ('|' in lines[a] and a + 1 < len(lines) and '---' in lines[a + 1])) :
                break
            paragraph_lines.append(lines[a].strip())
            a+=1
        
        if paragraph_lines :
            paragraph_text=' '.join(paragraph_lines)
            formatted_text=self._process_inline_formatting(paragraph_text)
            self.elements.append(Paragraph(formatted_text,self.styles['Normal']))
            self.elements.append(Spacer(1,0.1*inch))
        
        return a
    
    def _process_inline_formatting(self,text : str) -> str :
        """process inline markdown formatting."""
        # bold (**text** or __text__)
        text=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',text)
        text=re.sub(r'__(.*?)__',r'<b>\1</b>',text)
        
        # italic (*text* or _text_)
        text=re.sub(r'\*(.*?)\*',r'<a>\1</a>',text)
        text=re.sub(r'_(.*?)_',r'<a>\1</a>',text)

        # inline code (`code`)
        text=re.sub(r'`([^`]+)`',r'<font name="Courier" backColor="lightgrey">\1</font>',text)

        # Links [text](url)
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<link href="\2" color="blue">\1</link>',text)

        # strikethrough (~~text~~)
        text=re.sub(r'~~(.*?)~~',r'<strike>\1</strike>',text)

        return text

class MarkdownToPDFConverter :
    """main converter class that orchestrates the conversion process."""
    
    def __init__(self,page_size=letter,margin=0.75*inch) :
        self.page_size=page_size
        self.margin=margin
        self.parser=MarkdownParser()

    def convert_file(self,markdown_file : str , output_file : str=None) -> str :
        """convert a markdown file to PDF."""
        if not os.path.exists(markdown_file) :
            raise FileNotFoundError(f"Markdown file not found : {markdown_file}")
        
        with open(markdown_file,'r',encoding='utf-8') as f :
            markdown_content=f.read()
        
        if output_file is None :
            output_file=os.path.splitext(markdown_file)[0]+'.pdf'
        
        return self.convert_string(markdown_content,output_file)

    def convert_string(self,markdown_content : str,output_file : str)->str :
        """convert markdown string to PDF."""
        # parse markdown content
        elements=self.parser.parse_markdown(markdown_content)
        
        # create PDF document
        doc=SimpleDocTemplate(
            output_file,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # build PDF
        doc.build(elements)
        
        return output_file
    
    def preview_elements(self,markdown_content : str) -> List[str] :
        """preview the parsed elements (for debugging)."""
        elements=self.parser.parse_markdown(markdown_content)
        preview=[]

        for element in elements :
            if hasattr(element,'text'):
                preview.append(f"Paragraph : {element.text[:50]}...")
            elif hasattr(element,'_content'):
                preview.append(f"Table : {len(element._content)} rows")
            else:
                preview.append(f"Element : {type(element).__name__}")

        return preview

def main() :
    """command line interface for the converter."""



    parser = argparse.ArgumentParser(description='Convert Markdown files to PDF')
    parser.add_argument('input',help='Input markdown file')
    parser.add_argument('-o','--output', help='Output PDF file')
    parser.add_argument('-p','--page-size', choices=['letter', 'a4'], 
                       default='letter', help='Page size')
    parser.add_argument('-m','--margin', type=float, default=0.75, 
                       help='Page margin in inches')
    parser.add_argument('--preview',action='store_true', 
                       help='Preview parsed elements without generating PDF')
    
    args=parser.parse_args()
    
    # set page size
    page_size=A4 if args.page_size=='a4' else letter
    margin=args.margin*inch

    # create converter
    converter=MarkdownToPDFConverter(page_size=page_size,margin=margin)

    try :
        if args.preview :
            # preview mode
            with open(args.input,'r',encoding='utf-8') as f :
                content=f.read()
            
            elements=converter.preview_elements(content)
            print("Parsed Elements Preview :")
            print("-"*40)
            for a,element in enumerate(elements,1) :
                print(f"{a}. {element}")
        else :
            # convert's to PDF
            output_file=converter.convert_file(args.input,args.output)
            print(f"Successfully converted '{args.input}' to '{output_file}'")
            
    except Exception as e :
        print(f"Error : {e}",file=sys.stderr)
        sys.exit(1)

# example usage and testing
if __name__=="__main__" :
    # EXAMPLE IS TAKEN FROM AI, just for testing purposes
    # example markdown content for testing
    sample_markdown = """
# My Document Title

This is a **bold** statement and this is *italic* text. Here's some `inline code`.

## Section 2

Here's a blockquote:

> This is a quoted text that spans multiple lines
> and shows how blockquotes are rendered in PDF.

### Code Example

Here's a code block:

```python
def hello_world():
    print("Hello, World!")
    return True
```

### Lists

Unordered list:
- First item
- Second item with **bold** text
- Third item

Ordered list:
1. First numbered item
2. Second numbered item
3. Third numbered item

### Table Example

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Row 2    | More data| Final    |

### Links and Formatting

Check out [Python](https://python.org) for more information.

This text has ~~strikethrough~~ formatting.

---

## Final Section

This demonstrates various markdown features converted to PDF format.
"""
    
    # if running directly (not via command line), run example
    if len(sys.argv)==1 :
        print("Running example conversion.......////")

        # create example markdown file
        with open('example.md','w') as f:
            f.write(sample_markdown)

        # convert to PDF
        converter=MarkdownToPDFConverter()
        output_file=converter.convert_file('example.md','example.pdf')

        print(f"Example conversion complete : {output_file}")
        print("\nTo use from command line : ")
        print("python markdown_to_pdf.py input.md -o output.pdf")
    else :
        main()

# END OF CODE :)