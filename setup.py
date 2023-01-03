from setuptools import setup,find_packages

setup(
    name='OneManDevOpsSystem',
    version="0.1.0",
    author='RyomaChia',
    author_email="shindousaijia@hotmail.com",
    description="OneMan DevOps System",
    url="https://www.juliajia.com",
    classifiers=[
        "Programming Language :: Python :: 3.10.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires="==3.10.6",
    data_files=[('', ['requirements'])],
    py_modules=['manage']
      )