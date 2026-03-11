"""Views for handling Markdown to PDF conversion."""

import io
import logging
import os
import tempfile
import zipfile

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .backend.conversor import markdown_to_pdf

logger = logging.getLogger(__name__)


def markdown_to_pdf_view(request: HttpRequest) -> HttpResponse:
    """Convert a Markdown file to PDF.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The generated PDF file or the upload form.

    """
    if request.method == "POST" and request.FILES.get("markdown_file"):
        md_file = request.FILES["markdown_file"]
        output_name = request.POST.get("output_name", "output")
        pdf_buffer = io.BytesIO()

        try:
            temp_md_path = "/tmp/uploaded.md"
            with open(temp_md_path, "wb") as f:
                f.write(md_file.read())

            markdown_to_pdf(
                md_file_path=temp_md_path,
                pdf_file_path=pdf_buffer,
            )
            pdf_buffer.seek(0)
            response = HttpResponse(
                pdf_buffer,
                content_type="application/pdf",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{output_name}.pdf"'
            )
            return response

        except Exception as e:
            logger.error("Erro ao converter Markdown: %s", str(e))
            messages.error(
                request,
                f"Erro ao converter o arquivo: {e}",
            )
            return redirect("markdown_to_pdf")

    return render(request, "conversor/upload.html")


def markdown_zipped_to_pdf_view(request: HttpRequest) -> HttpResponse:
    """Convert a Markdown file from a ZIP archive to PDF.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The generated PDF file or the upload form.

    """
    if request.method == "POST" and request.FILES.get("zip_file"):
        zip_file = request.FILES["zip_file"]
        output_name = request.POST.get("output_name", "output")
        pdf_buffer = io.BytesIO()

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "upload.zip")
                with open(zip_path, "wb") as f:
                    for chunk in zip_file.chunks():
                        f.write(chunk)

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)

                markdown_file = None
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".md"):
                            markdown_file = os.path.join(root, file)
                            break
                    if markdown_file:
                        break

                if not markdown_file:
                    messages.error(
                        request,
                        "Nenhum arquivo Markdown (.md) encontrado no ZIP.",
                    )
                    return redirect("markdown_zipped_to_pdf")

                markdown_to_pdf(
                    md_file_path=markdown_file,
                    pdf_file_path=pdf_buffer,
                )

                pdf_buffer.seek(0)
                response = HttpResponse(
                    pdf_buffer,
                    content_type="application/pdf",
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="{output_name}.pdf"'
                )
                return response

        except Exception as e:
            logger.error("Erro ao converter ZIP: %s", str(e))
            messages.error(
                request,
                f"Erro ao processar o arquivo: {e}",
            )
            return redirect("markdown_zipped_to_pdf")

    return render(request, "conversor/upload_zip.html")
