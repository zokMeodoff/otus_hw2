from setuptools import setup, find_packages

setup(
    name='statistics_collector',
    version='1.0',
	description='Приложение для сбора и вывода статистики по наиболее часто встречающимся словам в исходном коде приложений',
    packages=find_packages(),
	install_requires=[
		'nltk ~= 3.4',
    ],
	entry_points={
        'console_scripts': ['csc=statistics_collector:main'],
    },
)