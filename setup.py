from setuptools import setup, find_packages
import versioneer

setup(
    name="jupyfuncs",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Jianxing Hu",
    author_email="jianxing.hu@xtalpi.com",
    description="XDL: XtalPi 深さ学習モデルの枠組み",
    url="www.xtalpi.com", 
    # packages=['jupyfuncs'],
    packages=find_packages(), 
    python_requires='>=3',
    data_files=[
        (
            'data_file', 
            [
                'funcs/defined_BaseFeatures.fdef',
                'funcs/datasets/vocab.txt'
            ]
        ),
    ],
    include_package_data=True
)