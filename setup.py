import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plastic",
    version="0.2.0",
    author="Andrew Geiger",
    author_email="andrew.geiger@corsosystems.com",
    description="An ORM interface that molds itself to your data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CorsoSource/plastic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
