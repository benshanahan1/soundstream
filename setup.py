from setuptools import setup, find_packages

setup(
    name='soundstream',
    version='0.1',
    description='Websocket server for real-time audio visualization.',
    url='http://github.com/benshanahan1/soundstream',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'flask',
        'flask_socketio',
        'sounddevice',
        'gevent',
    ],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
        ],
    },
    entry_points="""
        [console_scripts]
        soundstream=soundstream.__init__:main
    """,
)
