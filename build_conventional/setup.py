import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MAGIST-Algorithm",
    version="0.1.0",
    author="DeepShift Labs",
    author_email="krishna.shah@deepshift.dev",
    description="A powerful library for high-power, generally intelligent models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeepShift-Labs/MAGIST-Algorithm",
    project_urls={
        "Bug Tracker": "https://github.com/DeepShift-Labs/MAGIST-Algorithm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3 License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4==4.11.1",
        "Google_Images_Search==1.4.2",
        "matplotlib==3.5.1",
        "numpy==1.22.3",
        "pandas==1.4.1",
        "Pillow==9.1.1",
        "pymongo==3.12.3",
        "requests",
        "urllib3",
        "scikit_image==0.19.2",
        "scikit_learn==1.1.1",
        "selenium==4.2.0",
        "SpeechRecognition==3.8.1",
        "tensorflow==2.9.1",
        "tqdm==4.63.0",
        "wikipedia",
        "elasticsearch",
    ],
)
