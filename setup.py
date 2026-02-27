"""JASS 运行器的安装脚本。"""

from setuptools import setup, find_packages

setup(
    name="jass-runner",
    version="1.0.0",
    description="JASS 脚本模拟运行器，用于魔兽争霸 III",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="JASS 运行器团队",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "jass-runner=jass_runner.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
