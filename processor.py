from services.file_service import extract_uploaded_file


def process_file(file_path):
    """
    Process an uploaded study file and
    return cleaned extracted text.
    """

    if not file_path:
        raise ValueError("File path is required.")

    return extract_uploaded_file(file_path)