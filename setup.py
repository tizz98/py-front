from setuptools import setup


__version__ = "2.0.0"


setup(
    name="py-front",
    version=__version__,
    url="https://github.com/tizz98/py-front",
    download_url="https://github.com/tizz98/py-front/tarball/{version}".format(
        version=__version__,
    ),
    author="Elijah Wilson",
    author_email="elijah@elijahwilson.me",
    description="Simple API wrapper for Front.",
    long_description=open('README.md').read(),
    license="MIT",
    keywords="front api frontapp",
    install_requires=[
        "requests==2.20.1",
        "requests_toolbelt==0.8.0",
        "pytz==2018.7",
        "pyjwt==1.6.4",
    ],
    packages=[
        "front",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
)
