import os
from setuptools import find_packages, setup


with open('README.rst') as readme:
    long_description = readme.read()


def recursive_requirements(requirement_file, libs, links, path=''):
    if not requirement_file.startswith(path):
        requirement_file = os.path.join(path, requirement_file)
    with open(requirement_file) as requirements:
        for requirement in requirements.readlines():
            if requirement.startswith('-r'):
                requirement_file = requirement.split()[1]
                if not path:
                    path = requirement_file.rsplit('/', 1)[0]
                recursive_requirements(requirement_file, libs, links,
                                       path=path)
            elif requirement.startswith('-f'):
                links.append(requirement.split()[1])
            elif requirement.startswith('-e'):
                links.append(requirement.split()[1])
            else:
                libs.append(requirement)


libraries, dependency_links = [], []
recursive_requirements('requirements.txt', libraries, dependency_links)

setup(
    name='{{ project_name }}',
    version='0.1.0',
    packages=find_packages(),
    install_requires=libraries,
    dependency_links=dependency_links,
    long_description=long_description,
    description='',
    author='dnum-dip-unistra',
    author_email='dnum-dip@unistra.fr',
    maintainer='dnum-dip-unistra',
    maintainer_email='dnum-dip@unistra.fr',
    url='',
    download_url='',
    license='PSF',
    keywords=['django', 'Université de Strasbourg'],
    include_package_data=True,
)
