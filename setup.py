from setuptools import setup


setup(
    name='experpy',
    license='Apache 2.0',
    description='Track your experiment metric with git tags',
    author='Ben Davidson',
    author_email='ben.davidson6@googlemail.com',
    packages=['experpy'],
    install_requires=[
        'gitpython',
    ]
)