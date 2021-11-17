import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="p-stable-lsh-python",
    version="0.0.3",
    author="Charles7",
    author_email="liuhuiqi@mail.ustc.edu.cn",
    description="A 1&2-stable Locality-Sensitive Hashing implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CharlesLiu7/p-stable-lsh-python",
    project_urls={
        "Bug Tracker": "https://github.com/CharlesLiu7/p-stable-lsh-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['numpy', 'scipy']
)
