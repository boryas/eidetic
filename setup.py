from setuptools import setup, find_packages

setup(
    name='eidetic',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'rethinkdb',
    ],
    package_data = {
        '': ['*.md'],
    },
    author='Boris Burkov',
    author_email='b.burkov@gmail.com',

    entry_points='''
        [console_scripts]
        edtc=cli.edtc:cli
    ''',
)
