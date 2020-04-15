import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="maildir2mbox", 
    version="0.1",
    author="Philippe Fremy",
    author_email="phil.fremy@free.fr",
    description="Conversion of a mailbox in the maildir format to the mbox format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluebird75/maildir2mbox",
    py_modules=['maildir2mbox'],
    python_requires='>=3.5',
    
    license="Public Domain",
    keywords="maildir mbox",
    classifiers=[
        "Topic :: Communications :: Email",
        "License :: Public Domain",

        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)