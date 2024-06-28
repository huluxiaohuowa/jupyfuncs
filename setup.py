from setuptools import setup, find_packages
import setuptools_scm

# 自定义 version_scheme
def custom_version_scheme(version):
    """ 格式化版本号以排除任何开发后缀，并保持版本自动递增 """
    # 使用 'dirty' 表示未提交的更改
    if version.dirty:
        raise ValueError("Please commit your changes or stash them before building.")
    # 如果没有有效的标签，使用 '0.0.0' 作为基础版本号
    base_version = version.tag.base_version if version.tag else '0.0.0'
    # 检查是否有距离上一个标签的提交
    if version.distance is None or version.distance == 0:
        return base_version
    else:
        # 自动生成递增的版本号
        return f"{base_version}.{version.distance}"

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