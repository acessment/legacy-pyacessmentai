from setuptools import setup, find_packages

setup(
    name="pyacessmentai",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "google-cloud-texttospeech~=2.25.0",
        "google-genai~=1.36.0",
        "pydub~=0.25.1",
        "langchain>=1.0.0,<2.0.0",
        "langchain-core>=1.0.0,<2.0.0",
        "langchain-openai>=1.0.0,<2.0.0",
        "langchain-perplexity>=1.0.0,<2.0.0",
        "langchain-text-splitters>=1.0.0,<2.0.0",
        "weasyprint~=64.1.0",
        "Jinja2~=3.1.5",
        "python-dotenv~=1.0.1",
        "langchain-community",
        "nltk~=3.9.1",
        "spacy~=3.8.4",
        "pydantic~=2.12.4",
    ],
    entry_points={
        "console_scripts": [
            # Add your console scripts here
        ],
    },
    package_data={"pyacessmentai.static": ["*"], "pyacessmentai.schema": ["*"]},
    author="Sean Xiong",
    author_email="sean@acessment.ai",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/acessment/pyacessmentai",
    python_requires=">=3.9",
)
