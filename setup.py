import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tr064",
    version="0.0.1",
    author="Benjamin Füldner",
    author_email="benjamin@fueldner.net",
    description="TR-064 python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.fueldner.net/opensource/tr064",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
