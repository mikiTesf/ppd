import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pub_downloader",
    version="0.2",
    author="Mikyas Tesfamichael",
    author_email="mickyastesfamichael@gmail.com",
    description="Download 'periodic' Jehovah's Witnesses publications from the command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikiTesf/pd",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests', 'wget'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pub_downloader = pubd.pd:main'
        ]
    },
    python_requires='>=3.6',
)
