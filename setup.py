import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-bexio-auth',
    version='0.1',
    author="Netfire",
    author_email="info@netfire.ch",
    description="Python OAuth2 connector for Bexio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netfirech/python-bexio-auth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
