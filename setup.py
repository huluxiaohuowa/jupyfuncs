from setuptools import setup, find_packages
import versioneer

setup(
    name="jupyfuncs",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Jianxing Hu",
    author_email="hu.jx@outlook.com",
    description="jupyfuncs",
    # packages=['jupyfuncs'],
    packages=find_packages(), 
    python_requires='>=3',
    data_files=[
        (
            'data_file', 
            [
                'jupyfuncs/defined_BaseFeatures.fdef',
                'jupyfuncs/datasets/vocab.txt',
                'jupyfuncs/datasets/route_template.json'
            ]
        ),
    ],
    include_package_data=True
)