from setuptools import setup

setup(
    name='pandas_transform_checker',
    version='0.1',
    packages=['pandas_transform_checker'],
    url='https://github.com/thib-s/pandas_transform_checker',
    license='BSD 3-Clause License',
    install_requires=[
        'pandas'
    ],
    author='thibaut boissin',
    author_email='thibaut.boissin@gmail.com',
    description='function annotations to check properties on pandas dataframe transformations'
)
