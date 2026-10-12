from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename

from utils.pdf_utils import extract_pdf_text
from utils.ppt_utils import extract_ppt_text
from utils.docx_utils import extract_docx_text
from utils.text_utils import clean_text


# --------------------------------------------------
# SUPPORTED FILE TYPES
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".pptx",
    ".docx",
    ".txt"
}


# --------------------------------------------------
# CHECK WHETHER FILE TYPE IS ALLOWED
# --------------------------------------------------

def allowed_file(filename):
    """
    Check whether the uploaded file has
    a supported extension.
    """

    if not filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


# --------------------------------------------------
# SAVE UPLOADED FILE
# --------------------------------------------------

def save_uploaded_file(file_obj, target_dir):
    """
    Save an uploaded file safely inside the
    selected EXAMORA folder.
    """

    if file_obj is None:
        raise ValueError("No file was provided.")

    if not file_obj.filename:
        raise ValueError("File name is empty.")

    target_dir = Path(target_dir)

    # Create folder if it doesn't exist
    target_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Make filename safe
    original_filename = secure_filename(
        file_obj.filename
    )

    if not original_filename:
        raise ValueError(
            "Invalid file name."
        )

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    # Remove extension
    original_name = Path(
        original_filename
    ).stem

    # Limit filename length
    original_name = original_name[:80]

    # Generate unique ID
    unique_id = uuid4().hex[:8]

    # Example:
    # notes_a81f23cd.pdf
    final_filename = (
        f"{original_name}_{unique_id}"
        f"{extension}"
    )

    file_path = target_dir / final_filename

    # Save file
    file_obj.save(str(file_path))

    return file_path


# --------------------------------------------------
# EXTRACT TEXT FROM UPLOADED FILE
# --------------------------------------------------

def extract_uploaded_file(file_path):
    """
    Detect file type and extract readable text.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    # PDF
    if extension == ".pdf":
        text = extract_pdf_text(
            file_path
        )

    # PowerPoint
    elif extension == ".pptx":
        text = extract_ppt_text(
            file_path
        )

    # Word document
    elif extension == ".docx":
        text = extract_docx_text(
            file_path
        )

    # Text file
    elif extension == ".txt":
        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    # Clean extracted text
    return clean_text(text)


# --------------------------------------------------
# GET FILE INFORMATION
# --------------------------------------------------

def get_file_info(file_path):
    """
    Return basic information about an uploaded file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        return None

    return {
        "name": file_path.name,
        "extension": file_path.suffix.lower(),
        "size_bytes": file_path.stat().st_size,
        "path": str(file_path)
    }