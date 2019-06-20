import os
import sys
from setuptools import setup


if os.name == 'nt':
    extra_requires = ['cffi>=1.9.1']
    dependency_links = []
    package_data = {"sh": ["libsh.cp36-win_amd64.pyd"],
                    "tools3d": ["libspharm.cp36-win_amd64.pyd"]}
else:
    extra_requires = ['openexr>=1.3.0']
    dependency_links = ['https://github.com/jamesbowman/openexrpython/tarball/master#egg=openexr-1.3.0']
    if sys.version_info.major == 3:
        if sys.version_info.minor == 5:
            package_data = {"sh": ["libsh.cpython-35m-x86_64-linux-gnu.so"],
                    "tools3d": ["libspharm.cpython-35m-x86_64-linux-gnu.so"]}
        else:
            package_data = {"sh": ["libsh.cpython-37m-x86_64-linux-gnu.so"],
                    "tools3d": ["libspharm.cpython-37m-x86_64-linux-gnu.so"]}

setup(
    name='skylibs',
    description=('Tools to read, write, perform projections and handle LDR/HDR environment maps (IBL).'),
    author='Yannick Hold',
    author_email='yannickhold@gmail.com',
    license="LGPLv3",
    url='https://github.com/soravux/skylibs',
    version='0.4.1',
    packages=['ezexr', 'envmap', 'hdrio', 'hdrtools', 'hdrtools/tonemapping', 'sh', 'skydb', 'tools3d'],
    package_data=package_data,
    include_package_data=True,
    install_requires=['imageio>=1.6', 'rotlib>=0.91', 'tqdm', 'pyshtools'].extend(extra_requires),
    dependency_links=dependency_links,
)

