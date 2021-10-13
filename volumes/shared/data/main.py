#!/usr/bin/env python
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Demo data generation script.
"""

import os
import sys
import pdb as pdbpp
import traceback
import logging
from io import StringIO
from time import time
from proteus import config, Model, Wizard, ModelList

from .datasets import Datasets

log = logging.getLogger(__name__)
_colorless = os.environ.get('ENVIRONMENT') == "testing"


class ProteusStats():
    """Object manipulation statistics for proteus."""
    stats = {}

    @classmethod
    def start(cls):
        cls.reset()
        Model._original_save = Model.save
        Model._original_delete = Model.delete
        Model._original_duplicate = Model.duplicate
        ModelList._original_new = ModelList.new
        Wizard._original_execute = Wizard.execute
        Model.save = cls.save
        Model.delete = cls.delete
        Model.duplicate = cls.duplicate
        ModelList.new = cls.new
        Wizard.execute = cls.execute

    @classmethod
    def stop(cls):
        Model.save = Model._original_save
        Model.delete = Model._original_delete
        Model.duplicate = Model._original_duplicate
        ModelList.new = ModelList._original_new
        Wizard.execute = Wizard._original_execute
        del Model._original_save
        del Model._original_delete
        del Model._original_duplicate
        del ModelList._original_new
        del Wizard._original_execute

    @classmethod
    def reset(cls):
        cls.stats = {
            'created': {},
            'updated': {},
            'deleted': {},
            'duplicated': {},
            'executed': {},
        }

    @classmethod
    def track(cls, mode, model):
        """Count statistics."""
        if model not in cls.stats[mode]:
            cls.stats[mode][model] = 0
        cls.stats[mode][model] += 1

    @staticmethod
    def new(self, **kwargs):
        """Track entries created created by ModelList.new()."""
        new_record = ModelList._original_new(self, **kwargs)
        ProteusStats.track('created', new_record.__class__.__name__)
        return new_record

    @staticmethod
    def save(records):
        """Track entries created/updated by Model.save()."""
        if not isinstance(records, list):
            records = [records]
        for record in records:
            mode = record.id > 0 and 'updated' or 'created'
            ProteusStats.track(mode, record.__class__.__name__)
        Model._original_save(records)

    @staticmethod
    def delete(records):
        """Track entries deleted by Model.delete()."""
        if not isinstance(records, list):
            records = [records]
        for record in records:
            ProteusStats.track('deleted', record.__class__.__name__)
        Model._original_delete(records)

    @staticmethod
    def duplicate(records, default=None):
        """Track entries duplicated by Model.duplicate()."""
        if not isinstance(records, list):
            records = [records]
        for record in records:
            ProteusStats.track('duplicated', record.__class__.__name__)
        ids = Model._original_duplicate(records, default)
        return ids

    @staticmethod
    def execute(self, state):
        """Track wizards executed by Wizard.execute()."""
        ProteusStats.track('executed', '%s -> %s' % (self.name, state))
        Wizard._original_execute(self, state)


def color(text, status):
    """Colored output wrapper for stdout text."""
    if _colorless:
        return text
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
        self.stderr = sys.stderr
        sys.stdout = self.stringio = DebuggerAwareStringIO(self)
        sys.stderr = sys.stdout
        return self

    def __exit__(self, *args):
        self.extend(self.stringio.getvalue().splitlines())
        del self.stringio
        sys.stdout = self.stdout
        sys.stderr = self.stderr


def generate(datasets=[], excludes=[], reclimit=0,
             dependencies=True, leaves=True, pdb=False):
    """
    Generate datasets.

    Arguments:
    - datasets (list of strings)
    - excludes (list of strings)
    - reclimit (int): get debug level to reduce number of demodata records to
                      be generated per object, so db build time is reduced
    - dependencies (bool): Generate dependencies of given datasets.
    - leaves (bool): Generate given datasets.
    """

    if reclimit:
        reclimit = max(0, int(reclimit))

    # prepare datasets
    try:
        _datasets = datasets
        datasets = Datasets(datasets, excludes, dependencies, leaves)
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

    # setup ptvsd debugging
    vs_debug = int(os.environ.get('DEBUGGER_PTVSD'))
    if vs_debug:
        try:
            import ptvsd  # unconditional import breaks test coverage
            ptvsd.enable_attach(address=("0.0.0.0", 51006))
            # uncomment these  line(s), and select "Demodata Attach" in VS Code
            # if you need to debug datasets:
            ptvsd.wait_for_attach()
            # ptvsd.break_into_debugger()
        except Exception as ex:
            log.debug('ptvsd debugging not possible: %s' % ex)

    # configure output
    width = 100
    show_stats = True

    # start proteus tracking
    ProteusStats.start()

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
    print(color("  - reclimit: %s" % reclimit, "dim"))
    print(color("-" * width, "title"))

    # generate datasets
    error = ""
    exception = None
    total_start = time()
    if not datasets:
        print(color("Nothing to do.", "dim"))
    for dataset in datasets:

        # reset proteus tracking
        ProteusStats.reset()

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
                dataset.generate(reclimit)
        except Exception as e:
            error = "Error in dataset '%s':" % dataset
            exception = e
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
        if show_stats and not output.debugged:
            for mode in ProteusStats.stats:
                for model, num in ProteusStats.stats[mode].items():
                    print(color("  {0: >4} x ".format(num), "dim"), end="")
                    print(color("{0} ".format(model), "title"), end="")
                    print(color("{0}".format(mode), "dim"))
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
        raise exception
    msg = "Success."
    line = " " * (width - len(msg) - len(total_dur))
    print(color("-" * width, "title"))
    print(color(msg + line + total_dur, 'success'))

    # stop proteus tracking
    ProteusStats.stop()
