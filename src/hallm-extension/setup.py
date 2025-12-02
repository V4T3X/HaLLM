import os
from distutils.core import setup


def get_packages(rel_dir):
    packages = [rel_dir]
    for x in os.walk(rel_dir):
        # break into parts
        base = list(os.path.split(x[0]))
        if base[0] == "":
            del base[0]

        for mod_name in x[1]:
            packages.append(".".join(base + [mod_name]))

    return packages

setup(
    name='hallm',
    version='1.0',
    description='LLM-driven abstraction generation pipeline',
    author='Marco Spies',
    packages=get_packages('hallm'),
    entry_points={
        'console_scripts': [
            'hallm = hallm.main:main',
        ]
    },
    install_requires=[],
)
