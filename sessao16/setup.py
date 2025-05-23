from setuptools import setup, find_packages

setup(
    name="calculator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "build>=0.10.0",
            "twine>=4.0.2",
            "flake8>=6.0.0",
        ],
    },
    author="ETIC Backend II",
    author_email="example@example.com",
    description="A simple calculator package for CI/CD demonstration",
    keywords="calculator, ci, cd, github actions",
    python_requires=">=3.7",
    url="https://github.com/user/calculator",
    project_urls={
        "Bug Tracker": "https://github.com/user/calculator/issues",
        "Source Code": "https://github.com/user/calculator",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
