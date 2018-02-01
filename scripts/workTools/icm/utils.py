from os.path import expanduser, join
from workTools.icm.project import Project
import os


def getVersionFile(workdir):
    return join(workdir, '.dotfiles', 'gradle', 'version-mapping.yaml')


def checkProjectIsKnown(sets, componentset):
    if componentset not in sets:
        print("Component set or assembly with name '%s' not found." %
              (componentset))
        print("I have only these to offer:")
        print(str(sets.keys()))
        return False
    else:
        return True


def getProjects(names, data):
    sets = {}
    for setsName in names:
        if setsName not in data:
            print("Ignoring '%s' for further processing." % (setsName))
            continue
        if isProject(data[setsName]):
            sets[setsName] = Project(setsName, data[setsName])
        for projects in data:
            if 'includedIn' in data[projects] and data[projects]['includedIn'] == setsName:
                sets[setsName].addVersionRecommendation(
                    projects, data[projects]['versionRecom'])
    return sets


def isProject(versionMappingData):
    return "includedIn" not in versionMappingData


def isLinux():
    return os.name != 'nt'
