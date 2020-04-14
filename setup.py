import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="maildir2mbox", 
    version="0.1",
    author="Philippe Fremy",
    author_email="phil.fremy@free.fr",
    description="Conversion of mailbox in maildir format to mbox format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluebird75/maildir2mbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)