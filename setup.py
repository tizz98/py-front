from setuptools import setup


__version__ = "0.0.5"


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
    install_requires=open('requirements.txt').readlines(),
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
    ],
    zip_safe=True,
)
