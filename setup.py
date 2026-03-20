from setuptools import setup, find_packages

setup(
    name="easypygamewidgets",
    version="2.2.1",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "requests"
    ],
    include_package_data=True,
    package_data={
        "easypygamewidgets": [
            "assets/fonts/roboto mono/RobotoMono-Regular.ttf",
            "assets/fonts/roboto mono/OFL.txt",
            "assets/fonts/emoji/NotoEmoji-Regular.ttf",
            "assets/fonts/emoji/OFL.txt"
        ]
    },
    author="PizzaPost",
    description="Create GUIs for pygame.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PizzaPost/pywidgets ",
)
