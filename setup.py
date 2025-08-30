from setuptools import setup, find_packages

setup(
    name="oasm_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "urllib3>=1.26.0",
        "pytest>=7.0.0",
    ],
    python_requires=">=3.7",
)