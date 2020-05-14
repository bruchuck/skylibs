import os
import sys
import conda.cli.python_api as Conda


from setuptools import setup
version_string =  str(sys.version_info.major) + str(sys.version_info.minor)

if os.name == 'nt':
    extra_requires = ['cffi>=1.9.1']
    dependency_links = []
    package_data = {"sh": ["libsh.cp" + version_string +"-win_amd64.pyd"],
                    "tools3d": ["libspharm.cp" + version_string + "-win_amd64.pyd"]}
else:
    extra_requires = ['openexr>=1.3.0']
    dependency_links = ['https://github.com/jamesbowman/openexrpython/tarball/master#egg=openexr-1.3.0']
    package_data = {"sh": ["libsh.cpython-" + version_string + "m-x86_64-linux-gnu.so"], 
                    "tools3d": ["libspharm.cpython-"+ version_string +"m-x86_64-linux-gnu.so"]}


conda_install_packages = ['numpy', 'scipy', 'imageio', 'tqdm', 'cffi', 'astropy', 'pandas', 'xarray', 'matplotlib']
out = Conda.run_command("install", conda_install_packages)

setup(
    name='skylibs',
    description=('Tools to read, write, perform projections and handle LDR/HDR environment maps (IBL).'),
    author='Bruno Marques, Original author: Yannick Hold',
    author_email='chuckof@gmail.com',
    license="LGPLv3",
    url='https://github.com/bdorta/skylibs',
    version='0.5',
    packages=['ezexr', 'envmap', 'hdrio', 'hdrtools', 'hdrtools/tonemapping', 'sh', 'skydb', 'tools3d'],
    install_requires=['rotlib', 'pyshtools'],
    package_data=package_data,
    include_package_data=True,
    cffi_modules=["sh/build_sh.py:ffibuilder"]
)

