import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daphruler",
    version="0.3.0",
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
)