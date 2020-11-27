from setuptools import find_packages, setup

setup(
    name='master',
    author='Benjamin Rabier',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_dirs=["src"],
    install_requires=[
        'numpy==1.19.4',
        'tabulate==0.8.7',
        'yarn-api-client==1.0.2',
        'influxdb==5.3.1',
        'PyYAML==5.3.1',
        'scikit-learn==0.23.2'
    ],
    license='MIT',
    zip_safe=False,
)
