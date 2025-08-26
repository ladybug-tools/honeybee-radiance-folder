import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('cli-requirements.txt') as f:
    cli_requirements = f.read().splitlines()

setuptools.setup(
    name="honeybee-radiance-folder",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Honeybee Radiance folder is a Python library to read, write and "
    "validate Radiance folder structure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools/honeybee-radiance-folder",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[],
    extras_require={'cli': cli_requirements},
    include_package_data=True,
    entry_points={
        "console_scripts": ["honeybee-folder = honeybee_radiance_folder.cli:folder"]
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: IronPython",
        "Operating System :: OS Independent"
    ],
)
