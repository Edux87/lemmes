#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')

@task
def clean(ctx, bytecode=True, extra=''):
    patterns = [
        'build',
        'models/*',
        'temp/*',
        'tests/data/**/*.pickle'
    ]
    patterns.append('dist')
    patterns.append('*.egg*')

    if bytecode:
        patterns.append('**/*.pyc')
        patterns.append('**/**/*.pyc')
        patterns.append('**/**/**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        run("rm -rf %s" % pattern)

@task
def build(ctx, docs=False):
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")

@task(pre=[clean])
def test(ctx):
    run("python run_tests.py", pty=True)

@task(pre=[clean])
def acc(ctx, id=''):
    run("python run_accurancy.py", pty=True)
