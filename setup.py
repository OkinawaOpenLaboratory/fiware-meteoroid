import setuptools


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setuptools.setup(
    packages=setuptools.find_packages(),
    setup_requires=['pbr>=5.4.3'],
    pbr=True
)
