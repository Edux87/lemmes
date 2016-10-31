#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')


@task
def clean(ctx, bytecode=True, extra=''):
    patterns = []
    patterns.append('dist')
    patterns.append('*.egg*')

    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        run("rm -rf %s" % pattern)


@task(pre=[clean])
def build(ctx):
    run("python setup.py build && python setup.py egg_info")
    run("python setup.py sdist bdist_wheel")


@task
def pep8(ctx):
    run("pycodestyle --first --count --config=setup.cfg **/*.py")


@task(pre=[pep8, clean])
def test(ctx):
    run("python run_tests.py")


@task
def upload_test(pre=[build]):
    run("python setup.py register -r pypitest")
    run("python setup.py sdist upload -r pypitest")


@task
def upload_live(pre=[build]):
    run("python setup.py register -r pypi")
    run("python setup.py sdist upload -r pypi")
