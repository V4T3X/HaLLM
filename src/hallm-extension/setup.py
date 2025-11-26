from setuptools import setup, find_packages

setup(
    name='hallm',
    version='1.0',
    description='LLM-driven abstraction generation pipeline',
    author='Marco Spies',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hallm = hallm.main:main',
        ]
    },
    install_requires=[],
)
