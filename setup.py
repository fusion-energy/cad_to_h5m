import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cad_to_h5m",
    version="develop",
    author="The cad_to_h5m Development Team",
    author_email="mail@jshimwell.com",
    description="Converts CAD files to a DAGMC h5m file using Cubit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/cad_to_h5m",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=[
        "pytest",
    ],
    install_requires=["pytest"],
)
