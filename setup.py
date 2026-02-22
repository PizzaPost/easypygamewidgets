from setuptools import setup, find_packages

setup(
    name="easypygamewidgets",
    version="2.0.2",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "requests"
    ],
    author="PizzaPost",
    description="Create GUIs for pygame.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PizzaPost/pywidgets ",
)
