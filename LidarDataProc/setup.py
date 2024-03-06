from setuptools import setup


setup(
   name='LidarDataProc',
   version='0.1',
   description='Analyse a Lidar Scan "film" of a water surface (mainly the ocean) to determine informations about it, mainly the direction of the waves',
   author='MalCaor',
   author_email='xav.lemen@orange.fr',
   packages=['LidarDataProc'],  #same as name
   install_requires=['numpy'], #external packages as dependencies
)