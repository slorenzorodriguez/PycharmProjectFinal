from setuptools import setup

setup(
    name='SerWavesSkateCompany',
    version='1.0',
    author='Sergio Lorenzo Rodríguez',
    author_email='slorenzorodriguez@danielcastelao.org',
    packages=[''],
    url='https://www.danielcastelao.org',
    license='GLP',
    platforms="Unix",
    clasifiers=["Development Status :: 3 - Alpha",
                "Environment :: Console",
                "Topic :: Software Development :: Libraries",
                "License :: OSI Aproved :: GNU General Public License",
                "Programming Language :: Python :: 3.8",
                "Operating System :: Linux Ubuntu"
                ],
    description='Final Project Pycham DI',
    keywords="empaquetado instalador paquetes",
    #data_files=[('datos', ['dat/datos.txt'])],
    entry_points={'console_scripts': ['openProyect = proyecto.SerWaves: main', ], }
)
