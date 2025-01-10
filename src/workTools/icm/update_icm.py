from jinja2 import Environment
from workTools.icm.workdir import Workdir, Dirs
from workTools.icm.project import Project
from workTools.icm.utils import getProjects
from os import listdir
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def update(alias, workdir, versionMapFile):
    print('Updating '+workdir.workingDir())
    with open(versionMapFile) as fd:
        data = load(fd, Loader)
    sets = {}
    versionRecommendationFiles = []

    for assemblyName in listdir(workdir.file(Dirs.assemblies, '')):
        if assemblyName in data:
            sets[assemblyName] = Project(assemblyName, data[assemblyName])
            versionRecommendationFiles.extend(
                sets[assemblyName].getVersionRecommendationName())
        else:
            print("Ignoring assembly '%s' for update." % (assemblyName))

    sets = getProjects(listdir(workdir.file(Dirs.sets, '')), data)
    for cs in sets:
        versionRecommendationFiles.extend(
            sets[cs].getVersionRecommendationName())

    for cs in sets:
        if sets[cs].updateGit(workdir):
            sets[cs].fixVersionRecommendations(
                workdir, alias, versionRecommendationFiles)
