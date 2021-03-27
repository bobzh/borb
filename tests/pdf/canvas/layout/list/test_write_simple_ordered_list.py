import logging
import unittest
from pathlib import Path

from ptext.pdf.canvas.layout.list import OrderedList
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-simple-ordered-list.log"),
    level=logging.DEBUG,
)


class TestWriteSimpleOrderedList(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-simple-ordered-list")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        ul = OrderedList()
        ul.add(Paragraph(text="Lorem Ipsum Dolor Sit Amet Consectetur Nunc"))
        ul.add(Paragraph(text="Ipsum"))
        ul.add(Paragraph(text="Dolor"))
        ul.add(Paragraph(text="Sit"))
        ul.add(Paragraph(text="Amet"))

        layout = SingleColumnLayout(page)
        layout.add(ul)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
