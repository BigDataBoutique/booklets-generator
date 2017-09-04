import os
import types
import logging
from pprint import pprint

import click

dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)

# Loading the pyPdf Library
import pyPdf
from pyPdf import PdfFileWriter, PdfFileReader
from pyPdf.generic import RectangleObject


def findInDict(needle, haystack):
    for key in haystack.keys():
        try:
            value = haystack[key]
        except Exception:
            continue
        if key == needle:
            return value
        if isinstance(value, types.DictType) or isinstance(value, pyPdf.generic.DictionaryObject):
            x = findInDict(needle, value)
            if x is not None:
                return x


def add_pdf(full_path, output):
    pdf = PdfFileReader(open(full_path, "rb"))
    for page_num in xrange(pdf.numPages):
        output.addPage(pdf.getPage(page_num))


def generate(job_name, additional_dirs=None):
    print('Generating ' + job_name)

    if additional_dirs is None:
        additional_dirs = []

    output = PdfFileWriter()
    page_of_lines = PdfFileReader(open(dir_path + "/essentials/PageOfLines.pdf", 'rb')).getPage(0)

    cover = PdfFileReader(open(dir_path + "/essentials/%s.pdf" % job_name, 'rb'))
    output.addPage(cover.getPage(0))

    add_pdf(dir_path + "/essentials/cover-white-back.pdf", output)
    add_pdf(dir_path + "/essentials/cover_page.pdf", output)

    for dir in [dir_path + "/slides-" + job_name] + additional_dirs:
        for filename in os.listdir(dir):
            if os.path.isdir(filename) or not filename.endswith(".pdf"):
                continue

            if filename.startswith("X "):
                continue

            if filename.endswith(".slides.pdf"):
                pdf = PdfFileReader(open(os.path.join(dir, filename), "rb"))
                for page_num in xrange(pdf.numPages):
                    p = pdf.getPage(page_num)
                    p.scaleBy(0.8)
                    p.cropBox = p.mediaBox = p.artBox = p.trimBox = RectangleObject([30, 30, 450, 625])
                    output.addPage(p)
                    output.addPage(page_of_lines)
            elif filename.endswith(".pdf"):
                add_pdf(open(os.path.join(dir, filename)), output)

    output.addPage(page_of_lines)  # even out number of pages

    add_pdf(dir_path + "/essentials/survey.pdf", output)
    add_pdf(dir_path + "/essentials/back-cover.pdf", output)

    # Writing all the collected pages to a file
    with open(dir_path + "/final/%s.pdf" % job_name, "wb") as f:
        output.write(f)


generate("es-dev")
# generate("es-ops")
