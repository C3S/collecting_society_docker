# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

from importlib import import_module
import sys
import os


class Dataset():
    """Class wrapper for a dataset module."""
    def __init__(self, module):
        # sanity checks
        try:
            getattr(module, 'generate')
        except AttributeError:
            sys.exit("Error: generate() not in %s" % module.__name__)
        try:
            getattr(module, 'DEPENDS')
        except AttributeError:
            sys.exit("Error: DEPENDS not in %s" % module.__name__)
        # assign module
        self.module = module

    def __lt__(self, other):
        """Comparison function for sorting according to dependancies."""
        if str(self) in other.DEPENDS:
            return True
        try:
            for dependency in other.DEPENDS:
                if str(register[dependency]) in self.DEPENDS:
                    return False
                if self < register[dependency]:
                    return True
            for dependency in self.DEPENDS:
                if register[dependency] < other:
                    return True
        except RuntimeError:
            raise RuntimeError("Cirular dependancy: %s" % dependency)

    def __str__(self):
        """String function returning the last part of the module name."""
        return self.module.__name__.split('.')[-1]

    @property
    def __doc__(self):
        return self.module.__doc__

    @property
    def DEPENDS(self):
        return self.module.DEPENDS

    def generate(self):
        self.module.generate()


class Datasets(list):
    """Class for datasets."""
    def __init__(self, datasets=[], dependencies=True, leaves=True):
        """
        Initialized the datasets list with the given datasets.

        Arguments:
        - dependencies (bool): Add dependencies of given datasets.
        - leaves (bool): Add given datasets.
        """
        if not datasets:
            self.extend(register.values())
        else:
            # sanity checks
            if not dependencies and not leaves:
                return
            datasets = list(set(datasets))
            unknown = []
            for name in datasets:
                if name not in register:
                    unknown.append(name)
            if unknown:
                raise(LookupError(
                    "Dataset not found: %s" % ", ".join(unknown)))
            # add modules
            for name in datasets:
                if leaves:
                    self.append(register[name])
                if dependencies:
                    self.add_dependencies(register[name])

        # sort modules
        self.sort()

    def __str__(self):
        """Formats the list to use the dataset names."""
        return "[%s]" % ", ".join([str(m) for m in self])

    def add_dependencies(self, dataset):
        """Adds the dependent modules of dataset to the datasets list."""
        for dependency in dataset.DEPENDS:
            if register[dependency] in self:
                continue
            self.append(register[dependency])
            self.add_dependencies(register[dependency])


# register available datasets
# TODO: Security checks or static imports
register = {}
for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    # filter filenames
    if not filename.endswith(".py") or "__" in filename:
        continue
    # import module
    module_name = filename[:-3]
    module = import_module('.' + module_name, package='data.datasets')
    # register dataset module
    register[module_name] = Dataset(module)
