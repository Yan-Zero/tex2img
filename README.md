# tex2img

`tex2img` is a Python package that provides tools for rendering LaTeX documents as PDF files or PNG images using the `https://latex.ytotech.com/` API.

## Installation

You can install `tex2img` using `pip`:

```bash
pip install git+https://github.com/Yan-Zero/tex2img.git@main
```

## Usage

### Render LaTeX documents as PDF files

To render LaTeX documents as PDF files, you can use the `LatexCompiler` class:

```python
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
```

This code will compile the given LaTeX code into a PDF file and save it as `output.pdf`.

### Render LaTeX documents as PNG images

To render LaTeX documents as PNG images, you can use the `LatexRenderer` class:

```python
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
```

This code will compile the given LaTeX code into a PNG image and save it as `output.png`.

## Contributing

If you encounter any issues or have any suggestions for improvement,
please feel free to submit an issue or a pull request on GitHub at [tex2img](https://github.com/yan-zero/tex2img)

## License

`tex2img` is licensed under the Apache 2 License. See [LICENSE](LICENSE) for more information.
