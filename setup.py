# coding:utf-8


from setuptools import setup,find_packages

setup(
    name="TSDK",
    version = "0.1",
    install_requires = [
        'requests',
    ],
    # packages = find_packages(),
    packages = ['TSDK'],
    description = "淘宝爬虫SDK",
    long_description = "淘宝爬虫SDK",
    author = 'xinlingqudongX',
    author_email = 'aa@163.com',

    # license = 'GPL',
    # keywords = ('淘宝','SDK','爬虫'),
    # platforms = 'Independant',
    url = 'https://github.com/xinlingqudongX/TSDK',
    # data_files = ['./Api.json'],
)