import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checker-GilMelnik",
    version="1.0.0",
    author="Gil Melnik",
    author_email="gil@melnik.co.il",
    description="Tool dedicated to test python codes according to some test file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GilMelnik/checker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
