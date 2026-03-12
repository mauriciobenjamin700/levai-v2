"""Markdown to PDF converter using WeasyPrint."""

import os

import markdown
from weasyprint import HTML

from levai.apps.document.backend.styles.default import abnt


def markdown_to_pdf(
    md_file_path: str, pdf_file_path: str, css_file_path: str | None = None
) -> None:
    """Convert a Markdown file to PDF using WeasyPrint.

    Args:
        md_file_path (str): Path to the input Markdown file.
        pdf_file_path (str): Path to the output PDF file.
        css_file_path (str | None): Optional path to a CSS file for styling
            the PDF. Defaults to None, which uses the default ABNT style.

    Raises:
        FileNotFoundError: If the Markdown file does not exist.
        Exception: If reading the file or conversion fails.

    """
    try:
        with open(md_file_path, "r", encoding="utf-8") as f:
            md_content: str = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Erro: Arquivo '{md_file_path}' não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo: {e}")

    extensions: list[str] = [
        "fenced_code",
        "codehilite",
        "tables",
        "toc",
        "mdx_math",
        "attr_list",
        "footnotes",
        "pymdownx.arithmatex",
        "pymdownx.superfences",
    ]

    try:
        html_content: str = markdown.markdown(md_content, extensions=extensions)
    except Exception as e:
        raise Exception(f"Erro ao converter Markdown: {e}")

    base_path: str = os.path.dirname(md_file_path)
    html_content = html_content.replace('src="', f'src="{base_path}/')

    additional_css: str = ""
    if css_file_path and os.path.exists(css_file_path):
        try:
            with open(css_file_path, "r", encoding="utf-8") as f:
                additional_css = f.read()
        except Exception as e:
            print(f"Aviso: Não foi possível ler o arquivo CSS adicional: {e}")

    full_html: str = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{os.path.basename(md_file_path)}</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
            {abnt}
            {additional_css}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    try:
        print(f"Gerando PDF: {pdf_file_path}")
        HTML(string=full_html, base_url=base_path).write_pdf(pdf_file_path)
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
