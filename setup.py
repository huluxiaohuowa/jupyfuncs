from setuptools import setup, find_packages

def clean_version(version):
    """移除本地版本信息（如 `.dev` 后缀）"""
    base_version = version.tag.base_version if version.tag else '0.0.0'
    if version.distance:
        return f"{base_version}.post{version.distance}"
    return base_version

setup(
    name="jupyfuncs",
    use_scm_version={
        "local_scheme": "no-local-version",
        "version_scheme": clean_version,
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