from setuptools import setup, find_packages
import setuptools_scm

# 自定义 version_scheme
def clean_version_scheme(version):
    """只返回基于标签的版本号，不添加任何开发后缀。"""
    return version.format_with("{tag}")

setup(
    name="jupyfuncs",
    use_scm_version={
        "local_scheme": "no-local-version",
        "version_scheme": clean_version_scheme,
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