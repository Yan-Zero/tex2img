r""" Module to compile LaTeX code to PNG file. 

This module provides a `Latex2PNG` class that can be used to render LaTeX
documents.

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
        """ Compile LaTeX code to PNG file. 

        Parameters
        ----------
        latex_code : str
            LaTeX code to compile.
        images : list[tuple[str, str]], optional
            List of images to include in the PDF file, by default None
        compiler : str, optional
            LaTeX compiler to use, by default 'lualatex'

        Returns
        -------
        list[bytes]
            List of PNG files.

        Raises
        ------
        CompilationError
            If the compilation failed.
        """
        png_results = []
        pdf = super().compile(latex_code, images, compiler)
        with BytesIO(pdf) as pdf_file:
            for i in pdf2image.convert_from_bytes(pdf_file.read()):
                with BytesIO() as png_bytes:
                    i.save(png_bytes, 'PNG')
                    png_results.append(png_bytes.getvalue())
        return png_results


class AsyncLatex2PNG(AsyncLatexCompiler):
    """ Class to compile LaTeX code to PNG file asynchronously.

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
        """ Compile LaTeX code to PNG file asynchronously.

        Parameters
        ----------
        latex_code : str
            LaTeX code to compile.
        images : list[tuple[str, str]], optional
            List of images to include in the PDF file, by default None
        compiler : str, optional
            LaTeX compiler to use, by default 'lualatex'

        Returns
        -------
        list[bytes]
            List of PNG files.

        Raises
        ------
        CompilationError
            If the compilation failed.
        """
        png_results = []
        pdf = await super().acompile(latex_code, images, compiler)
        with BytesIO(pdf) as pdf_file:
            for i in pdf2image.convert_from_bytes(pdf_file.read()):
                with BytesIO() as png_bytes:
                    i.save(png_bytes, 'PNG')
                    png_results.append(png_bytes.getvalue())
        return png_results
