from setuptools import setup

install_requires = [
    'numpy',
    'matplotlib',
    'nose',
]

packages = [
    'nakametpy',
    'tests'
]

console_scripts = [
    # 'sample_lib_cli=sample_lib_cli.call:main',
]


setup(
    name='nakametpy',
    python_requires='>3.6.0',
    # version='0.1.0', # (2021.01.19)
    version='0.2.5', # (2021.02.18)
    description='Meteorological modules for calculation and colormap.',
    packages=packages,
    install_requires=install_requires,
    url = 'https://github.com/muchojp/NakaMetPy',
    author = 'Yuki Nakamura',
    author_email = 'contact.muchiwo@gmail.com',
    # entry_points={'console_scripts': console_scripts},
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type="text/markdown",
)
