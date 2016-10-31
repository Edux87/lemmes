# -*- coding: utf-8 -*-
'''
The main test runner script.
Usage: ::
    python run_tests.py
Skip slow tests
    python run_tests.py fast
When there's no Internet
    python run_tests.py no-internet
'''
from __future__ import unicode_literals
import nose
import sys


def main():
    args = get_argv()
    success = nose.run(argv=args)
    sys.exit(0) if success else sys.exit(1)


def get_argv():
    args = [sys.argv[0], "tests", '--verbosity', '2']
    attr_conditions = []
    attr_conditions.append("not skip")
    attr_expression = " and ".join(attr_conditions)
    if attr_expression:
        args.extend(["-A", attr_expression])
    return args


if __name__ == '__main__':
    main()
