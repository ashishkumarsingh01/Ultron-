"""
Setup script for Ultron.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ultron-agent",
    version="0.1.0",
    author="Ultron Team",
    author_email="ultron@example.com",
    description="Advanced AI Agent Kernel with multi-modal capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashishkumarsingh01/Ultron-",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "openai>=1.3.0",
        "requests>=2.31.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "chromadb>=0.4.0",
    ],
    extras_require={
        "voice": ["speech-recognition>=3.10.0", "pyttsx3>=2.90"],
        "vision": ["opencv-python>=4.8.0", "pillow>=10.0.0", "easyocr>=1.7.0"],
        "web": ["selenium>=4.15.0", "beautifulsoup4>=4.12.0"],
        "dev": ["pytest>=7.4.0", "black>=23.12.0", "mypy>=1.7.0"],
    },
    entry_points={
        "console_scripts": [
            "ultron=examples.run_server:main",
        ],
    },
)
