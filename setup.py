from setuptools import setup, find_packages

setup(
    name="resetty",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    license="MIT",
    description="Django Middleware that requires a user to reset password",
    url="https://github.com/banzai-io/resetty/",
    author="Ignacio De La Madrid",
    author_email="ignacio@getbanzai.com",
    install_requires=["django==2.2.11"],
)
