from setuptools import setup, find_packages

setup(
    name="easypygamewidgets",
    version="26.12",
    author="PizzaPost",
    author_email="pizzapost.mail@gmail.com",
    description="Create GUIs for pygame.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PizzaPost/pywidgets ",
    license="MIT",
    license_files=[
        "LICENSE",
        "easypygamewidgets/assets/fonts/roboto mono/OFL.txt",
        "easypygamewidgets/assets/fonts/emoji/OFL.txt"
    ],
    keywords=["pygame", "gui", "widgets", "library", "pygame library", "pygame widgets"],
    platforms=["any"],
    project_urls={
        "Examples": "https://github.com/PizzaPost/pywidgets/tree/master/examples",
        "Repository": "https://github.com/PizzaPost/pywidgets",
        "Issues": "https://github.com/PizzaPost/pywidgets/issues"
    },
    python_requires=">=3.6",  # vermin easypygamewidgets/
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: pygame",
        "Topic :: Games/Entertainment",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English"
    ],
    install_requires=[
        "pygame-ce",
        "requests"
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "easypygamewidgets": [
            "assets/fonts/roboto mono/RobotoMono-Regular.ttf",
            "assets/fonts/roboto mono/OFL.txt",
            "assets/fonts/emoji/NotoEmoji-Regular.ttf",
            "assets/fonts/emoji/OFL.txt",
            "assets/tooltip/info.png",
            "assets/tooltip/warning.png",
            "assets/tooltip/blocked.png"
        ]
    }
)
