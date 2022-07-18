from setuptools import setup

setup(
    name='diff_unpack',
    version='1.1.0',
    description='A ChRIS DS plugin that is a thin wrapper about diff_unpack (part of TrackVis, original author Ruopeng Wang)',
    author='FNNDSC',
    author_email='rudolph.pienaar@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-diff_un',
    py_modules=['diff_unpack'],
    install_requires=['chris_plugin'],
    license='MIT',
    python_requires='>=3.8.2',
    packages=['init', 'job'],
    entry_points={
        'console_scripts': [
            'diff_unpack = diff_unpack:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1',
            'pytest-mock~=3.8'
        ]
    }
)
