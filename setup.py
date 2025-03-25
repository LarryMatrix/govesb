from setuptools import setup, find_packages

setup(
    name="govesb",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Lawrance Massanja",
    description="A Python library for supporting GovESB Integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LarryMatrix",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)