
import setuptools


setuptools.setup(
     name='easy_deploy',
     version='0.1',
     install_requires=['pyyaml'],
     scripts=['scripts/easy_deploy'] ,
     author="Matt Strozyk",
     author_email="mstrozyk25@gmail.com",
     description="Deploy configuration to remote hosts",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
