from setuptools import setup

setup(
    name='Pynity',
    version='1.6.17',
    packages=['Core', 'Core.math', 'Core.scene', 'Core.objects', 'Core.components', 'Core.networking'],
    url='',
    license='',
    author='KeyFr4me',
    author_email='',
    description='2D unity-like programming with Python and Pygame',
    install_requires=["colorama>=0.4.3", "pycryptodome~=3.9.7", "pygame~=1.9.6"]
)
