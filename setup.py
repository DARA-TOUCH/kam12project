from setuptools import setup, find_packages

setup(
    name='kam12-baseactions',
    version='0.1.0',
    description='Description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dara TOUCH',
    author_email='touchdara2015@live.com',
    url='https://github.com/yourusername/kam12-baseactions',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.1',
        'pandas>= 2.2.1',
        'openpy= 3.1.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)