from setuptools import setup

setup(
   name='Silcon store admin panel',
   version='1.0',
   description='Admin panel for online shopping mall',
   author='Abolo Samuel',
   author_email='ikabolo59@gmail.com',
   packages=['ssa'],  #same as name
   install_requires=['gunicorn', 'requests', 'flask', 'flask-cors', 'pandas', 'pymysql'], #external packages as dependencies
)
