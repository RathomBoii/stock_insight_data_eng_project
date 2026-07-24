from setuptools import find_namespace_packages, setup


setup(
    name="data-platform-clean-ohlc",
    version="0.1.0",
    packages=find_namespace_packages(
        include=["domains*", "infrastructures*", "usecases*"]
    ),
)