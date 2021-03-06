from setuptools import setup

requires = [
    "flask",
    "flask-sqlalchemy",
    "psycopg2",
]


setup(
    name="paywu",
    version="0.1",
    maintainer="Onyedika Ndife",
    maintainer_email="onyedikandife@gmail.com",
    description="U-Gateway POS PAYMENT Solution",
    packages=["app"],
    include_package_data=True,
    install_requires=requires,
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
    ],
)
