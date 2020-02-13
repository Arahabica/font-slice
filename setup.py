from setuptools import setup, find_packages


def _requirements():
    with open("requirements.txt", "r") as f:
        return [name.strip() for name in f.readlines()]


with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="font-subset-css",
    version="0.0.1",
    description="font subset and css generator",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Sasage Ryuji",
    author_email="r.sasage@gmail.com",
    url="https://github.com/Arahabica/font-subset-css",
    license="MIT",
    packages=find_packages(exclude=("tests")),
    install_requires=_requirements(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development"
    ],
    entry_points={
        'console_scripts': [
            'fontsubsetcss = fontsubsetcss.main:main',
        ],
    },
    include_package_data=True
)
