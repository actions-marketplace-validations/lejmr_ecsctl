from setuptools import setup

setup(
    name='ecsctl',
    version='0.1.0',
    packages=['ecs', 'ecs.bin'],
    install_requires=[
        'Click',
        'Jinja2',
        'python-magic',
        'python-slugify',
        'dateparser',
        'boto3',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'ecsctl = ecs.bin.ecsctl:group',
        ],
    },
)