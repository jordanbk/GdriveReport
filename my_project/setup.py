from setuptools import setup, find_packages

setup(
    name='gdrive_project',   # Replace with your project name
    version='0.1',
    packages=find_packages(where='my_project'),  # Adjust the path to your project folder
    install_requires=[  # Add your dependencies here
        'google-api-python-client',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
    ],
    entry_points={
        'console_scripts': [
            'gdrive_program = my_project.__main__:main'  # This defines the command to run the project
        ],
    },
)
