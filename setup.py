from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1',
    packages=find_packages(where='my_project/src'),  # This points to the correct 'src' folder
    package_dir={'': 'my_project/src'},  # This indicates that packages are in 'my_project/src'
    install_requires=[
        'google-api-python-client',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
    ],
    entry_points={
        'console_scripts': [
            'gdrive_program=src.__main__:main',  # Fully qualified path to your main function
        ],
    },
)
