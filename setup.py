"""Lucifer's Screwdriver: Machine Learning Near Earth Object Identifier

Lucifer's Screwdriver is a project created for the NASA Space Apps 2016
challenge: "Near Earth Objects Machine Learning".
"""

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Programming Language :: Python
Programming Language :: Python :: 3
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Topic :: Scientific/Engineering :: Astronomy
Topic :: Scientific/Engineering :: Machine Learning
"""

MAJOR      = 0
MINOR      = 1
MICRO      = 0
ISRELEASED = False
VERSION    = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def get_version_info():
    FULLVERSION = VERSION

    if not ISRELEASED:
        FULLVERSION += '-dev'

    return FULLVERSION

__version__ = get_version_info()


def setup_package():
    metadata = dict(
        name='lucifers_screwdriver',
        url='https://github.com/lucifers-screwdriver/lucifers-screwdriver',
        description=DOCLINES[0],
        long_description="\n".join(DOCLINES[2:]),
        version=__version__,
        package_dir={'': 'src'},
        packages=['lucifers_screwdriver'],
        keywords=[
            'astronomy',
            'machine learning',
            'near earth object',
        ],
        classifiers=[f for f in CLASSIFIERS.split('\n') if f],
        entry_points={
            "console_scripts" : [
                "lucifers-screwdriver = lucifers_screwdriver.cli:main"
            ]
        },
        install_requires=[
            'numpy>=1.10.0',
            'matplotlib>=1.5.0',
#            'pandas>=0.18.0',
            'scipy>=0.17.0',
            'scikit-learn>=0.17.1',
        ]
    )

    from setuptools import setup

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
