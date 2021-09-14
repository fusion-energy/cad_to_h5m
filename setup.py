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
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    tests_require=[
        "pytest",
         "dagmc_h5m_file_inspector"
    ],
    python_requires='>=3.6',
    install_requires=["pytest"],
)
