from setuptools import setup, find_packages
import setuptools_scm

def custom_version_scheme(version):
    """自定义版本号方案，确保没有 .dev 后缀"""
    if version.tag:
        return version.format_with("{tag}")
    else:
        return "0.0.0"

setup(
    name="jupyfuncs",
    use_scm_version={
        "local_scheme": "no-local-version",
        "version_scheme": custom_version_scheme,
        "write_to": "jupyfuncs/_version.py"
    },
    author="Jianxing Hu",
    author_email="hu.jx@outlook.com",
    description="A collection of functions for Jupyter notebooks",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/huluxiaohuowa/jupyfuncs",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['setuptools_scm']
)