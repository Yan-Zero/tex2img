r""" Module to render LaTeX code to PDF file. 

This module provides a `LatexCompiler` class that can be used to render LaTeX
documents as PDF files.

Example usage:

    from tex2img import LatexCompiler

    renderer = LatexCompiler()
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
    pdf_data = renderer.compile(tex)
    with open('output.pdf', 'wb') as f:
        f.write(pdf_data)
"""

import os
import base64
import json
from typing import Optional
import requests
import aiofiles
import aiohttp
from .exceptions import CompilationError


class LatexCompiler:
    '''Class to compile LaTeX code to PDF file.
    Methods
    -------
    compile(latex_code, images=None, compiler='lualatex')
        Compile LaTeX code to PDF file.
    '''

    api_url: str

    session: requests.Session

    def __init__(self, api_url: str = ""):
        """ Initialize the class.

        Parameters
        ----------
        api_url : str, optional
            URL of the LaTeX compiler API, by default os.getenv('LATEX_COMPILER_API_URL', '')
            RECOMMENDED: https://latex.ytotech.com/builds/sync
        """
        self.session = requests.Session()
        if not api_url:
            api_url = os.getenv('LATEX_COMPILER_API_URL', '')
        if not api_url:
            raise ValueError("API_URL cannot be empty.")
        self.api_url = api_url

    def compile(self, latex_code,
                images: Optional[list[tuple[str, str]]] = None,
                compiler='lualatex'):
        '''Compile LaTeX code to PDF file.

        Parameters
        ----------
        latex_code : str
            LaTeX code to compile.
        images : list[tuple[str, str]], optional
            List of images to include in the PDF, by default None.
            Format: [(path, content), ...]
                The content can be a base64 encoded string, file path or URL. 
        compiler : str, optional
            Compiler to use, by default 'lualatex'

        Returns
        -------
        pdf_data : bytes
            PDF file data.

        Raises
        ------
        CompilationError
            If compilation fails.
        '''
        main_doc = {
            'main': True,
            'content': latex_code
        }

        resources = [main_doc]
        if images:
            for path, content in images:
                if content.startswith('http'):
                    resources.append({
                        'path': path,
                        'url': content
                    })
                    continue
                if os.path.isfile(content):
                    with open(content, 'rb') as f:
                        content = base64.b64encode(f.read()).decode('utf-8')
                resources.append({
                    'path': path,
                    'content': content
                })

        payload = {
            'compiler': compiler,
            'resources': resources
        }
        response = self.session.post(self.api_url, data=json.dumps(payload), headers={
            'Content-Type': 'application/json'}, timeout=60)
        if response.status_code in [200, 201]:
            pdf_data = response.content
            return pdf_data
        else:
            error_logs = response.json()['logs']
            raise CompilationError(
                f"Compilation failed with error logs: {error_logs}")


class AsyncLatexCompiler(LatexCompiler):
    """Class to compile LaTeX code to PDF file asynchronously.

    Methods
    -------
    acompile(latex_code, images=None, compiler='lualatex')
        Compile LaTeX code to PDF file.
    """

    session: aiohttp.ClientSession

    def __init__(self, api_url: str = ""):
        super().__init__(api_url=api_url)
        self.session = aiohttp.ClientSession()

    def compile(self, latex_code, images: list[tuple[str, str]] | None = None, compiler='lualatex'):
        """ DON'T USE THIS METHOD. USE `acompile` INSTEAD. """
        raise NotImplementedError("Use acompile instead.")

    async def acompile(self, latex_code,
                       images: Optional[list[tuple[str, str]]] = None,
                       compiler='lualatex'):
        """Asynchronous version of compile method.

        Parameters
        ----------
        latex_code : str
            LaTeX code to compile.
        images : list[tuple[str, str]], optional
            List of images to include in the PDF, by default None.
            Format: [(path, content), ...]
                The content can be a base64 encoded string, file path or URL.
        compiler : str, optional
            Compiler to use, by default 'lualatex'

        Returns
        -------
        pdf_data : bytes
            PDF file data.

        Raises
        ------
        CompilationError
            If compilation fails.
        """
        main_doc = {
            'main': True,
            'content': latex_code
        }

        resources = [main_doc]
        if images:
            for path, content in images:
                if content.startswith('http'):
                    resources.append({
                        'path': path,
                        'url': content
                    })
                    continue
                if os.path.isfile(content):
                    async with aiofiles.open(content, 'rb') as f:
                        content = base64.b64encode(await f.read()).decode('utf-8')
                resources.append({
                    'path': path,
                    'content': content
                })

        payload = {
            'compiler': compiler,
            'resources': resources
        }
        async with self.session.post(self.api_url, data=json.dumps(payload), headers={
                'Content-Type': 'application/json'}, timeout=60) as response:
            if response.status in [200, 201]:
                pdf_data = await response.read()
                return pdf_data
            else:
                error_logs = (await response.json())['logs']
                raise CompilationError(
                    f"Compilation failed with error logs: {error_logs}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
