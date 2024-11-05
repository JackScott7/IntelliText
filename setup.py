from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="IntelliText",
    version="0.1.0",
    author="Jack Scott",
    author_email="cloner.bl12@gmail.com",
    description="IntelliText is a powerful, customizable keyboard macro and text expansion tool"
                " that helps you automate repetitive typing tasks and execute custom actions."
                " It's designed to boost your productivity by allowing you to create shortcuts"
                " for frequently used text, commands, and actions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JackScott7/intellitext",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: General",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyperclip>=1.8.2",
        "pynput>=1.7.6",
    ],
    entry_points={
        "console_scripts": [
            "intellitext=intellitext:main",
        ],
    },
)