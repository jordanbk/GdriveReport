from setuptools import setup, find_packages

def parse_requirements(filename):
    """ Load requirements from a pip requirements file """
    with open(filename, 'r') as f:
        return f.read().splitlines()

setup(
    name='reports',
    version='0.1',
    packages=find_packages(),  # Automatically finds all packages (gdrive and reports)
    install_requires=parse_requirements('requirements.txt'),  # Load dependencies from requirements.txt
    entry_points={
        'console_scripts': [
            'gdrivereports=main:main',  # Entry point to your main script function
        ],
    },
)
