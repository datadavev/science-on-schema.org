from setuptools import setup, find_packages

kwargs = {
    'name': 'soso',
    'version': '0.1.0',
    'description': 'Tools and ',
    'author': 'Dave Vieglais',
    'url': 'https://github.com/datadavev/science-on-schema.org/validation/tools',
    'license': 'Apache License, Version 2.0',
    'packages': find_packages(),
    'package_data': {},
    'install_requires': [
        'rdflib',
        'rdflib-jsonld',
        'pyshacl',
        'click'
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    'keywords': (
        'schema.org', 'data', 'dataset',
    ),
    'entry_points': {
        'console_scripts': [
            'soso=soso:main'
        ],
    }
}
setup(**kwargs)
