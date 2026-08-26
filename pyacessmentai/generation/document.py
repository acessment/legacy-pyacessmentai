import io
from jinja2 import Template
from weasyprint import HTML, Document
from importlib import resources
from pyacessmentai import static


template = Template(resources.read_text(static, "template_mega_panel.html"))


def makePDF(
    exercise_json,
    isSolution=False,
    show_index=True,
    return_b64=False,
    watermark_image=None,
    watermark_text=None,
    header=None,
    footer=None,
    font_size="md",
    header_image_size=18
) -> io.BytesIO:
    # Get the base URL path safely
    with resources.path(static, "template_mega_panel.html") as template_path:
        base_url = str(template_path.parent)

    if header is None:
        header = watermark_image
    if footer is None:
        footer = watermark_text

    header_image = None
    header_text = None
    footer_image = None
    footer_text = None

    # Check header type and assign appropriate values
    if header:
        if header.startswith("data:image/"):
            # Base64 encoded image
            header_image = header
        elif "." in header and any(header.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"]):
            # Filename
            header_image = header
        else:
            # Text
            header_text = header

    # Check footer type and assign appropriate values
    if footer:
        if footer.startswith("data:image/"):
            # Base64 encoded image
            footer_image = footer
        elif "." in footer and any(footer.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"]):
            # Filename
            footer_image = footer
        else:
            # Text
            footer_text = footer

    if watermark_image and not watermark_image.startswith("data:image/"):
        watermark_image = f"file:///{base_url}/{watermark_image}".replace(":", "%3A").replace("\\", "/")

    print(f"Base URL: {base_url}")

    exercise_pdf = io.BytesIO()
    exercise_html = template.render(
        render_queue=exercise_json,
        isSolution=isSolution,
        show_index=show_index,
        watermark_image=watermark_image,
        watermark_text=watermark_text,
        header_image=header_image,
        header_text=header_text,
        footer_image=footer_image,
        footer_text=footer_text,
        font_size=font_size,
        header_image_size=f"height: {header_image_size}px",
    )

    HTML(
        string=exercise_html,
        base_url=base_url,
    ).write_pdf(exercise_pdf)
    exercise_pdf.seek(0)
    if return_b64:
        import base64

        exercise_pdf_b64 = base64.b64encode(exercise_pdf.read()).decode("utf-8")
        exercise_pdf.close()
        return f"data:application/pdf;base64,{exercise_pdf_b64}"
    else:
        return exercise_pdf


def renderPDFdoc(exercise_json, isSolution=False, show_index=True, hasLineNumber=False) -> Document:
    exercise_html = template.render(render_queue=exercise_json, isSolution=isSolution, show_index=show_index, hasLineNumber=hasLineNumber)

    # Get the base URL path safely
    with resources.path(static, "template_mega_panel.html") as template_path:
        base_url = str(template_path.parent)

    doc = HTML(
        string=exercise_html,
        base_url=base_url,
    ).render()
    return doc
