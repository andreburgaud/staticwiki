import pathlib
from setuptools import setup

CWD = pathlib.Path(__file__).parent

README = (CWD / "README.md").read_text()

setup(
    name="staticwiki",
    version="0.1.0",
    description="Static Site Generator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/andreburgaud/staticwiki",
    author="Andre Burgaud",
    author_email="andre.burgaud@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["staticwiki"],
    entry_points={
        "console_scripts": [
            "staticwiki=staticwiki.__main__:main",
        ]
    },
)
