import os
import subprocess
import shutil

from setuptools.command.install import install as InstallCommand
from setuptools import setup

CHDKPTP_PATH = os.path.abspath(os.path.join('.', 'chdkptp', 'vendor',
                                            'chdkptp'))
CHDKPTP_PATCH = os.path.abspath(os.path.join('.', 'chdkptp_module.diff'))


class CustomInstall(InstallCommand):
    def run(self):
        print("Patching and building chdkptp...")
        subprocess.check_call(['patch', '-f', '-d', CHDKPTP_PATH, '-i',
                               CHDKPTP_PATCH, '-p', '1'])
        os.symlink(os.path.join(CHDKPTP_PATH, 'config-sample-linux.mk'),
                   os.path.join(CHDKPTP_PATH, 'config.mk'))
        subprocess.check_call(['make', '-C', CHDKPTP_PATH])

        filenames = next(os.walk(CHDKPTP_PATH), (None, None, []))[2]
        print("Files after compilation")
        print(filenames)
        InstallCommand.run(self)

setup(
    name='chdkptp.py',
    version="0.1.4",
    description=("Python bindings for chdkptp"),
    author="Johannes Baiter",
    url="http://github.com/jbaiter/chdkptp.py.git",
    author_email="johannes.baiter@gmail.com",
    license='GPL',
    packages=['chdkptp'],
    package_dir={'chdkptp': 'chdkptp'},
    package_data={"chdkptp": ["vendor/chdkptp/chdkptp.so",
                              "vendor/chdkptp/lua/*.lua"]},
    install_requires=[
        "lupa >= 1.6"
    ],
    cmdclass={'install': CustomInstall}
)
