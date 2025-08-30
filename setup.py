from setuptools import setup, find_packages

setup(
    name="oasm-sdk",
    version="0.1.3",
    packages=find_packages(include=['oasm_sdk', 'oasm_sdk.*']),
    install_requires=[
         "requests>=2.31.0",
         "urllib3>=1.26.0",
    ],
    description="Python SDK for OASM platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="OASM",
    author_email="tuanthanh2kk4@gmail.com",
    url="https://github.com/oasm/oasm-sdk-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)