import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dynamic-raw-sql",
    version="0.0.2",
    author="Ben Lee",
    description="A simple and flexible way to work with raw SQL queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["dynamic_raw_sql"],
    package_dir={"":"."},
    install_requires=[],
    project_urls={
        'Source': 'https://github.com/benlee1284/dynamic-raw-sql',
        'Tracker': 'https://github.com/benlee1284/dynamic-raw-sql/issues',
    },
)
