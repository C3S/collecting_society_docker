# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

from importlib import import_module
import sys
import os


csv_delimiter = ','
csv_quotechar = '"'
csv_devlimit = 25
test_text = (
    "Lorem ipsum dolor sit amet, consetetur diam nonumy eirmod tempor "
    "invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. "
    "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita "
    "kasd gubergren.\n\nLorem ipsum.\n\nSea takimata sanctus est Lorem "
    "ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur "
    "sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore "
    "et dolore magna aliquyam erat, sed diam voluptua. At vero eos et "
    "accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, "
    "no sea takimata sanctus est Lorem ipsum dolor sit amet."
)


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
        self.name = self.module.__name__.split('.')[-1]
        self.dependson = []
        self.dependencyof = []

    def __str__(self):
        """String function returning the last part of the module name."""
        return self.name

    @property
    def __doc__(self):
        return self.module.__doc__

    @property
    def DEPENDS(self):
        return self.module.DEPENDS

    def generate(self, reclimit):
        self.module.generate(reclimit)

    def add_dependencies(self, module_name):
        for dependency in register[module_name].DEPENDS:
            if dependency not in self.dependson:
                self.dependson.append(dependency)
            if self.name not in register[dependency].dependencyof:
                register[dependency].dependencyof.append(self.name)
            self.add_dependencies(dependency)


class Datasets(list):
    """Class for datasets."""
    def __init__(self, datasets=[], excludes=[],
                 dependencies=True, leaves=True):
        """
        Initialized the datasets list with the given datasets.

        Arguments:
        - datasets (list): List of datasets to add.
        - excludes (list): List of datasets to exclude.
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
                raise LookupError("Dataset not found: %s" % ", ".join(unknown))
            # add modules
            for name in datasets:
                if leaves:
                    self.append(register[name])
                if dependencies:
                    self.add_dependencies(register[name])

        # sort modules
        self.sort_dependencies()

        # exclude modules
        if excludes:
            excludes = list(set(excludes))
            unknown = []
            for name in excludes:
                if name not in register:
                    unknown.append(name)
            if unknown:
                raise LookupError("Dataset not found: %s" % ", ".join(unknown))
            # remove modules
            for name in excludes:
                if register[name] in self:
                    self.remove(register[name])
                self.remove_dependencies(register[name])

    def __str__(self):
        """Formats the list to use the dataset names."""
        return "[%s]" % ", ".join([m.name for m in self])

    def add_dependencies(self, dataset):
        """Adds the dependent modules of dataset to the datasets list."""
        for dependency in dataset.DEPENDS:
            if register[dependency] in self:
                continue
            self.append(register[dependency])
            self.add_dependencies(register[dependency])

    def remove_dependencies(self, dataset):
        """Removes the dependent modules of dataset from the datasets list."""
        for dependency in dataset.DEPENDS:
            if register[dependency] in self:
                self.remove(register[dependency])
            self.remove_dependencies(register[dependency])

    def sort_dependencies(self):
        self.sort(key=lambda x: len(x.dependson), reverse=True)
        datasets = []
        while self:
            dataset = self.pop()
            index = 0
            for i, other in enumerate(datasets):
                if dataset.name in other.dependencyof:
                    index = i + 1
            datasets.insert(index, dataset)
        self.extend(datasets)


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
# calculate dependencies
for module_name, dataset in register.items():
    dataset.add_dependencies(module_name)
