"""TR-064 setuptools configuration."""

import setuptools
import tr064

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tr064",
    version=tr064.__version__,
    description="TR-064 python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="TR-064 LAN DSL CPE configuration broadband forum home router",
    license="MIT",
    author="Benjamin Füldner",
    author_email="benjamin@fueldner.net",
    url="https://github.com/bfueldner/tr064",
    project_urls={
        'Source': 'https://github.com/bfueldner/tr064',
        'Bug Reports': 'https://github.com/bfueldner/tr064/issues',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'lxml'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
