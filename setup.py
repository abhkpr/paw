from setuptools import setup, find_packages

setup(
    name="paw",
    version="0.1.0",
    description="local AI commit message generator using ollama",
    author="Abhishek Kumar",
    url="https://github.com/abhkpr/paw",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "paw=paw.__main__:main",
        ],
    },
)
