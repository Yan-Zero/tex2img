from tex2img import Latex2PNG, LatexCompiler


def test_latex_compiler():
    renderer = LatexCompiler()
    TEX = r'''
    \documentclass{article}
    \usepackage{amsmath}
    \begin{document}
    This is a LaTeX document.
    \[
        \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    \]
    \end{document}
    '''

    pdf_data = renderer.compile(TEX)
    assert pdf_data is not None


def test_latex2png():
    renderer = Latex2PNG()
    TEX = r'''
    \documentclass{article}
    \usepackage{amsmath}
    \begin{document}
    This is a LaTeX document.
    \[
        \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    \]
    \end{document}
    '''

    png_data = renderer.compile(TEX)
    assert png_data is not None
