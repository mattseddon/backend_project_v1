from setuptools import setup

setup(
    name='backend_server',
    packages=['backend_server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'sqlalchemy',
        'pymysql',
        'sqlalchemy-utils',
        'flask-restful',
        'datetime',
        'flask-marshmallow',
        'marshmallow-sqlalchemy'
    ],
)