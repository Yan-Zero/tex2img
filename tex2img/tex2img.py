r""" Module to compile LaTeX code to PNG file. 

This module also provides a `Latex2PNG` class that can be used to render LaTeX
documents as PNG images using the `https://latex.ytotech.com/` API.

Example usage:

    from tex2img import Latex2PNG

    renderer = Latex2PNG()
    tex = r'''
    \documentclass{article}
    \usepackage{amsmath}
    \begin{document}
    This is a LaTeX document.
    \[
        \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    \]
    \end{document}
    '''
    png_data = renderer.compile(tex)
    with open('output.png', 'wb') as f:
        f.write(png_data)
"""

from io import BytesIO
import pdf2image.pdf2image as pdf2image
from .latex_compiler import LatexCompiler, AsyncLatexCompiler


class Latex2PNG(LatexCompiler):
    """ Class to compile LaTeX code to PNG file. 
    Only first page of the PDF file is converted to PNG.

    Attributes
    ----------
    API_URL : str
        URL of the LaTeX compiler API.

    Methods
    -------
    compile(latex_code, images=None, compiler='lualatex')
        Compile LaTeX code to PNG file.
    """

    def compile(self, latex_code, images: list[tuple[str, str]] | None = None, compiler='lualatex'):
        pdf = super().compile(latex_code, images, compiler)
        with BytesIO(pdf) as pdf_file:
            with BytesIO() as png_bytes:
                png_image = pdf2image.convert_from_bytes(pdf_file.read())[0]
                png_image.save(png_bytes, 'PNG')
                return png_bytes.getvalue()


class AsyncLatex2PNG(AsyncLatexCompiler):
    """ Class to compile LaTeX code to PNG file asynchronously.
    Only first page of the PDF file is converted to PNG.

    Attributes
    ----------
    API_URL : str
        URL of the LaTeX compiler API.

    Methods
    -------
    acompile(latex_code, images=None, compiler='lualatex')
        Compile LaTeX code to PNG file.
    """

    def compile(self, latex_code,
                images: list[tuple[str, str]] | None = None,
                compiler='lualatex'):
        raise NotImplementedError("Use acompile instead.")

    async def acompile(self, latex_code,
                       images: list[tuple[str, str]] | None = None,
                       compiler='lualatex'):
        pdf = await super().acompile(latex_code, images, compiler)
        with BytesIO(pdf) as pdf_file:
            with BytesIO() as png_bytes:
                png_image = pdf2image.convert_from_bytes(pdf_file.read())[0]
                png_image.save(png_bytes, 'PNG')
                return png_bytes.getvalue()
