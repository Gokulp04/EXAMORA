from pathlib import Path

from pypdf import PdfReader


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file_path):
    """
    Extract text from all pages of a PDF file.

    Parameters
    ----------
    file_path : str or Path
        Path of the PDF file.

    Returns
    -------
    str
        Extracted text.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    try:
        reader = PdfReader(str(file_path))

        pages_text = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            try:
                page_text = page.extract_text()

                if page_text:
                    pages_text.append(
                        f"\n--- Page {page_number} ---\n"
                    )

                    pages_text.append(page_text)

            except Exception as error:

                print(
                    f"Warning: Could not read page "
                    f"{page_number}: {error}"
                )

        return "\n".join(pages_text).strip()

    except Exception as error:

        raise RuntimeError(
            f"Unable to process PDF: {error}"
        )