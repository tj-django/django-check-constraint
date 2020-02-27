import os
import io

from setuptools import find_packages, setup

install_requires = ["Django>=2.2.10"]

test_requires = [
    "nox==2019.11.9",
    "pluggy>=0.7",
    "mock==2.0.0",
    "unittest-xml-reporting==2.5.2",
    "codacy-coverage==1.3.11",
]

deploy_requires = [
    "bump2version==1.0.0",
    "readme_renderer[md]",
    "changes==0.7.0",
    "git-changelog==0.1.0",
    "twine==1.3.1",
]

lint_requires = [
    "flake8==3.4.1",
    "yamllint==1.10.0",
    "isort==4.2.15",
    "pre-commit==2.0.1",
]

local_dev_requires = [
    "pip-tools==4.4.1",
    "check-manifest==0.37",
    "psycopg2>=2.5.4",
    "mysqlclient>=1.3.13",
]

extras_require = {
    "development": [local_dev_requires, install_requires, test_requires, lint_requires],
    "test": test_requires,
    "lint": lint_requires,
    "deploy": deploy_requires,
    "nox": test_requires,
}

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, "README.md")
LONG_DESCRIPTION_TYPE = "text/markdown"

if os.path.isfile(README_PATH):
    with io.open(README_PATH, encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = ""

VERSION = (1, 0, 18)

version = ".".join(map(str, VERSION))

setup(
    name="django-check-constraint",
    version=version,
    description="Extends django check constraint to support annotations.",
    python_requires=">=3.5",
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    author="Tonye Jack",
    author_email="jtonye@ymail.com",
    maintainer="Tonye Jack",
    maintainer_email="jtonye@ymail.com",
    url="https://github.com/jackton1/django-check-constraint",
    license="MIT/Apache-2.0",
    keywords=[
        "django",
        "django-check-constraint",
        "django check constraint",
        "check constraint-django",
        "model constraints",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
    ],
    install_requires=install_requires,
    tests_require=["coverage"],
    extras_require=extras_require,
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "demo"]
    ),
)
