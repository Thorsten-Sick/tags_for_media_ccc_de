import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tags_for_media_ccc_de-Thorsten_Sick", # Replace with your own username
    version="0.0.1",
    author="Thorsten Sick",
    author_email="thorsten.sick@email.de",
    description="Generate tags and offer a search REPL interface for CCC media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Thorsten-Sick/tags_for_media_ccc_de",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)