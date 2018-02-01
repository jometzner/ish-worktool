from subprocess import run, CalledProcessError
from yaml import load
from workTools.icm.project import Project
from workTools.icm.workdir import Workdir, Dirs
from os.path import exists, join
from os import environ
from workTools.icm.utils import checkProjectIsKnown, isProject, isLinux


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def buildAll(workdir, alias, versionMapFile):
    with open(versionMapFile) as fd:
        data = load(fd, Loader)

    for project in data:
        if canBeBuilt(data[project], project, workdir):
            print("")
            print(str(project).upper())
            print("")
            if not build(workdir, alias, project, versionMapFile):
                break


def build(workdir, alias, componentset, versionMapFile):
    with open(versionMapFile) as fd:
        data = load(fd, Loader)
    sets = {}
    for name in data:
        if canBeBuilt(data[name], name, workdir):
            sets[name] = Project(name, data[name])
    if not checkProjectIsKnown(sets, componentset):
        return False
    try:
        processEnv = {
            'GRADLE_USER_HOME': workdir.file(Dirs.gradle, '')}
        for keys in environ:
            processEnv[keys] = environ[keys]

        if not sets[componentset].isAssembly():
            run([gradlew(workdir, sets[componentset]), 'publish'], cwd=workdir.file(
                Dirs.sets, componentset), check=True, env=processEnv)
        else:
            run([gradlew(workdir, sets[componentset]), 'publish'], cwd=workdir.file(
                Dirs.assemblies, componentset), check=True, env=processEnv)
    except CalledProcessError as identifier:
        print(identifier)
        return False
    return True


def canBeBuilt(versionMappingData, name, workdir):
    if not isProject(versionMappingData):
        return False
    p = Project(name, versionMappingData)
    if not p.isAssembly():
        return exists(workdir.file(Dirs.sets, name))
    else:
        return exists(workdir.file(
            Dirs.assemblies, name))


def gradlew(workdir, project):
    if isLinux():
        return './gradlew'
    else:
        if project.isAssembly():
            return join(workdir.file(Dirs.assemblies, project.name), 'gradlew.bat')
        else:
            return join(workdir.file(Dirs.sets, project.name), 'gradlew.bat')
