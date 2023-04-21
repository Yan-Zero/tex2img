from setuptools import setup, find_packages

setup(
    name="tex2img",
    version="0.1.2",
    author="Yan",
    author_email="1964649083@qq.com",
    description="A package for rendering LaTeX documents as PDF files or PNG images.",
    packages=find_packages(),
    install_requires=[
        "aiofiles",
        "aiohttp",
        "requests",
        "pdf2image",
    ],
)
