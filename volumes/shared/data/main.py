#!/usr/bin/env python
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Demo data generation script.
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import pdb as pdbpp
import traceback
from StringIO import StringIO
from time import time
from proteus import config, Model

from datasets import Datasets


def color(text, status):
    """Colored output wrapper for stdout text."""
    text = str(text)
    if status == 'error':
        text = "\033[1m\033[5m\033[91m" + text
    elif status == 'success':
        text = "\033[1m\033[32m" + text
    elif status == 'output':
        text = "\033[94m" + text
    elif status == 'title':
        text = "\033[1m\033[33m" + text
    elif status == 'subtitle':
        text = "\033[35m" + text
    elif status == 'dim':
        text = "\033[2m" + text
    text += "\033[0m"
    return text


class DebuggerAwareStringIO(StringIO, object):
    """StringIO, that restores sys.stdout on debugging."""
    def __init__(self, context, *args, **kwargs):
        self.context = context
        super(DebuggerAwareStringIO, self).__init__(*args, **kwargs)

    def write(self, *args, **kwargs):
        if sys.gettrace():
            sys.stdout = self.context.stdout
            if not self.context.debugged:
                sys.stdout.write("\n\n")
                for line in self.context.stringio.getvalue().splitlines():
                    sys.stdout.write(line)
                self.context.debugged = True
                self.context.stringio = StringIO()
                sys.stdout.write("\n\n")
            sys.stdout.write(*args, **kwargs)
            return
        super(DebuggerAwareStringIO, self).write(*args, **kwargs)


class Capturing(list):
    """Capture stdout for later output."""
    def __enter__(self):
        self.debugged = False
        self.stdout = sys.stdout
        sys.stdout = self.stringio = DebuggerAwareStringIO(self)
        return self

    def __exit__(self, *args):
        self.extend(self.stringio.getvalue().splitlines())
        del self.stringio
        sys.stdout = self.stdout


def generate(datasets=[], dependencies=True, leaves=True, pdb=False):
    """
    Generate datasets.

    Arguments:
    - dependencies (bool): Generate dependencies of given datasets.
    - leaves (bool): Generate given datasets.
    """
    # prepare datasets
    try:
        _datasets = datasets
        datasets = Datasets(datasets, dependencies, leaves)
    except (LookupError, RuntimeError) as e:
        sys.exit(color(e, "error"))

    # setup tryton
    cfg = config.set_trytond(config_file=os.environ.get('TRYTOND_CONFIG'))
    try:
        # set company context, if company was already created
        Company = Model.get('company.company')
        context = cfg.get_context()
        context['company'] = Company(1).id
        cfg._context = context
    except Exception:
        pass

    # configure output width
    width = 100

    # print header
    modes = []
    if dependencies:
        modes.append("dependencies")
    if leaves:
        modes.append("leaves")
    modes = " and ".join(modes)
    db_name = os.environ.get('DB_NAME')
    print()
    print(color("-" * width, "title"))
    print(color("  Generate datasets", "title"))
    print(color("  - datasets:", "dim"), end="")
    if _datasets:
        print(color(" %s" % modes, "dim"), end="")
        print(color(" of [%s]" % ", ".join(_datasets), "dim"))
    else:
        print(color(" all", "dim"))
    print(color("  - database: %s" % db_name, "dim"))
    print(color("-" * width, "title"))

    # generate datasets
    error = ""
    total_start = time()
    if not datasets:
        print(color("Nothing to do.", "dim"))
    for dataset in datasets:

        # print dataset title
        set_start = time()
        bullet = "> "
        title = "%s" % dataset
        doc = dataset.__doc__.strip().split("\n")[0].strip()
        if doc:
            title += ":"
            if len(bullet) + len(title) + len(doc) > width - 10:
                trail = " (...) "
                doc_length = width - len(bullet) - len(title) - len(trail) - 10
                doc = doc[:doc_length] + trail
        title += " "
        doc += " "
        print(color(bullet, 'title'), end='')
        print(color(title, 'subtitle'), end='')
        if doc:
            print(color("%s" % doc, 'dim'), end='')

        # generate dataset
        output = []
        try:
            with Capturing() as output:
                dataset.generate()
        except Exception:
            error = "Error in dataset '%s':" % dataset
            if pdb:
                print("\n")
                output.debugged = True
                extype, value, tb = sys.exc_info()
                traceback.print_exc()
                print("")
                pdbpp.post_mortem(tb)

        # print captured output and dataset benchmark
        set_end = time()
        dur = " {:.0f} s".format(set_end - set_start)
        line = "." * (width - len(bullet) - len(title) - len(doc) - len(dur))
        if output.debugged:
            line = "." * (width - len(dur))
        print(color(line + dur, "dim"))
        if output:
            print("")
            for line in output:
                print(color("  " + line, 'output'))
            print("")

        # stop on error
        if error:
            break

    # print footer
    total_end = time()
    total_dur = " {:.0f} s".format(total_end - total_start)
    if error:
        print(color(error, "error"))
        raise
    msg = "Success."
    line = " " * (width - len(msg) - len(total_dur))
    print(color("-" * width, "title"))
    print(color(msg + line + total_dur, 'success'))
