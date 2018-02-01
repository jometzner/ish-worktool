import jinja2 as template
from os import mkdir, rmdir
from os.path import expanduser, join, exists
from yaml import load
from workTools.icm.project import Project
from workTools.icm.workdir import Workdir
from workTools.icm.utils import checkProjectIsKnown, getProjects

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def addComponentset(workdir, alias, componentset, versionMapFile):
    with open(versionMapFile) as file:
        data = load(file, Loader)
    sets = getProjects(data.keys(), data)

    if not checkProjectIsKnown(sets, componentset):
        return False

    if sets[componentset].checkoutInto(workdir):
        sets[componentset].versionRecommendation(workdir, alias)
