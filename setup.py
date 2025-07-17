from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cctv-analyzer",
    version="0.1.0",
    author="Taouil Fatima ezzahrae - Salmane Koraichi",
    author_email="taouilfatimaezzahrae@gmail.com",
    description="Automated CCTV footage analysis and highlight generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Strawberry404/CCTV",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "gpu": [
            "torch>=1.9.0",
            "torchvision>=0.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cctv-analyze=cctv_analyzer.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cctv_analyzer": ["config/*.yaml"],
    },
)
