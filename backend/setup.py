from setuptools import find_packages, setup

setup(
    name="semantic-search-chatbot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "jinja2>=3.0.0",
        "python-multipart>=0.0.5",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "chromadb>=0.4.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A semantic search chatbot with multiple LLM providers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
