from setuptools import setup, find_packages
import setuptools_scm

def custom_version_scheme(version):
    """自定义版本号方案，确保没有 .dev 后缀"""
    if version.exact:
        return version.format_with("{tag}")
    elif version.distance:
        return f"{version.format_next_version()}.post{version.distance}"
    else:
        return version.format_with("0.0.0")

def custom_local_scheme(version):
    """自定义本地版本方案，确保没有本地版本后缀"""
    return ""

setup(
    name="jupyfuncs",
    use_scm_version={
        "version_scheme": custom_version_scheme,
        "local_scheme": custom_local_scheme,
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
