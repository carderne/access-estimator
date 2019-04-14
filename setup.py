from distutils.core import setup

import gridfinder

long_description = """
Estimate electricity access on a raster basis worldwide.
"""

setup(
    name="accessestimator",
    version=gridfinder.__version__,
    author="Chris Arderne",
    author_email="chris@rdrn.me",
    description="Estimate electricity access on a raster basis worldwide",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carderne/accessestimator",
    packages=["accessestimator"],
    install_requires=["gridfinder", "numpy>=1.2.0", "rasterio>=1.0.18"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
