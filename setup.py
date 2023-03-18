import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daphruler",
    version="0.3.3",
    author="Nelson Stevens",
    author_email="nelson.stevens92@gmail.com",
    description="Automate collecting morphometric traits of zooplankton.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nelstevens/The-Daphnia-ruler",
    project_urls={
        "Bug Tracker": "https://github.com/nelstevens/The-Daphnia-ruler/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "astroid==2.3.3",
        "attrs==21.2.0",
        "cycler==0.10.0",
        "decorator==4.4.1",
        "imageio==2.6.1",
        "iniconfig==1.1.1",
        "isort==4.3.21",
        "kiwisolver==1.1.0",
        "lazy-object-proxy==1.4.3",
        "matplotlib==3.1.2",
        "mccabe==0.6.1",
        "networkx==2.4",
        "numpy==1.17.4",
        "opencv-python==4.1.2.30",
        "packaging==21.0",
        "pandas==0.25.3",
        "Pillow==6.2.1",
        "pluggy==1.0.0",
        "py==1.10.0",
        "pylint==2.4.4",
        "pyparsing==2.4.5",
        "pytest==6.2.5",
        "python-dateutil==2.8.1",
        "pytz==2019.3",
        "PyWavelets==1.1.1",
        "scikit-image==0.16.2",
        "scipy==1.3.3",
        "six==1.13.0",
        "toml==0.10.2",
        "tqdm==4.40.2",
        "typed-ast==1.4.0",
        "wrapt==1.11.2"
    ],
)
