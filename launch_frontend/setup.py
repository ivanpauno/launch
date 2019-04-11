from setuptools import find_packages
from setuptools import setup

setup(
    name='launch_frontend',
    version='0.7.3',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools'],
    zip_safe=True,
    author='Dirk Thomas',
    author_email='dthomas@osrfoundation.org',
    maintainer='Dirk Thomas',
    maintainer_email='dthomas@osrfoundation.org',
    url='https://github.com/ros2/launch',
    download_url='https://github.com/ros2/launch/releases',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Launch process from different front-ends.',
    long_description=(
        'This package provides the to parse different front-ends '
        'to a programmatic launch process.'),
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
)
