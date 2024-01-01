from setuptools import setup

setup(
    name="passbox",
    version="0.10",
    description="encrypt message or files for you",
    author="summerlove66",
    url="https://github.com/summerlove66/passbox.git",
    py_modules=['passbox'],
    install_requires=["click>=8.0.1",],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'passbox = passbox:cli',
        ],
    },
)
