import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from utils.pdf_utils import extract_pdf_text


class TestPDFUtils(unittest.TestCase):

    def test_missing_pdf(self):
        with self.assertRaises(FileNotFoundError):

            extract_pdf_text(
                Path("this_file_does_not_exist.pdf")
            )


if __name__ == "__main__":
    unittest.main()