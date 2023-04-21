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
    assert pdf_data[:4] == b'%PDF'


def test_latex2png():
    renderer = Latex2PNG()
    TEX = r'''
    \documentclass{ctexart}
    \usepackage{amsmath}
    \pagestyle{empty}
    \begin{document}
    $(x+y)^8$的展开式和前面的$(1-\frac{y}{x})$相乘得到$x^2 y^6$这一项，$x^2 y^6$怎么来的呢，只能是$1\cdot x^2 y^6 - \frac{y}{x} \cdot x^3 y^5$。第一项是$\binom{8}{2}$，第二项是$\binom{8}{3}$！

    \end{document}
    '''

    png_data = renderer.compile(TEX, compiler='lualatex')
    assert png_data[:4] == b'\x89PNG'
