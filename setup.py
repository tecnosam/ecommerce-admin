from setuptools import setup

setup(
   name='Silcon store backend',
   version='1.0',
   description='Backend for online shopping mall',
   author='Abolo Samuel',
   author_email='ikabolo59@gmail.com',
   packages=['ssb'],  #same as name
   install_requires=['gunicorn', 'requests', 'flask', 'numpy', 'flask-cors', 'pandas', 'pymysql', 'stripe'], #external packages as dependencies
)
