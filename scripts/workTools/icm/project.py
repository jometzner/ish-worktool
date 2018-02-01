from git import Repo
from os.path import join, exists
from os import mkdir
from workTools.icm.workdir import Workdir, Dirs
from shutil import copyfile


class Project(object):
    def __init__(self, name, versionMappinObj):
        self.name = name
        if 'assembly' in versionMappinObj:
            self.assembly = versionMappinObj['assembly']
        else:
            self.assembly = False
        self.versions = {}
        self.branches = {}
        self.dependson = []
        self.versionRecomFileNames = []
        for version in versionMappinObj['versions']:
            self.versions[version] = versionMappinObj['versions'][version]
            self.branches[self.versions[version]] = version

        self.git = versionMappinObj['git']
        self.dependson = versionMappinObj['dependson']
        if 'versionRecom' in versionMappinObj:
            self.versionRecomFileNames.append(versionMappinObj['versionRecom'])

    def isAssembly(self):
        return self.assembly

    def checkoutInto(self, workDir):
        if workDir.version not in self.versions:
            return False
        try:
            if not self.isAssembly():
                repo = Repo.init(workDir.file(Dirs.sets, self.name))
            else:
                repo = Repo.init(workDir.file(Dirs.assemblies, self.name))
            try:
                origin = repo.remote('origin')
            except ValueError:
                origin = repo.create_remote('origin', self.git)

            origin.fetch()
            for upstreamRef in origin.refs:
                if upstreamRef.remote_head in self.branches and self.versions[workDir.version] == upstreamRef.remote_head:
                    headRef = repo.create_head(
                        self.versions[workDir.version], upstreamRef)
                    headRef.set_tracking_branch(upstreamRef)
                    headRef.checkout()
            if not repo.head.is_valid():
                print("Preparing git repo hasn't completed successfully \
(HEAD pointer points nowhere) Probably a misconfiguration of the version\
-mapping.yaml file.")
                return False
            repo.close()
            return True
        except IOError as error:
            print(error)
            return False

    def versionRecommendation(self, workDir, staticVersion):
        if not self.isAssembly():
            setHomeDir = workDir.file(Dirs.sets, self.name)
        else:
            setHomeDir = workDir.file(Dirs.assemblies, self.name)

        if not exists(setHomeDir):
            print("Component set %s hasn't been checked out yet." % (self.name))
            return

        buildConfigDir = join(setHomeDir, 'build')
        if not exists(buildConfigDir):
            mkdir(buildConfigDir)

        scmversion = join(buildConfigDir, 'scmversion')
        if not exists(scmversion):
            mkdir(scmversion)

        with open(join(scmversion, 'static.version'), 'w') as f:
            f.write(staticVersion)

        versionRecommendation = join(buildConfigDir, 'versionRecommendation')
        if not exists(versionRecommendation):
            mkdir(versionRecommendation)

        for deps in self.dependson:
            if exists(join(setHomeDir, deps)):
                copyfile(join(setHomeDir, deps), join(
                    versionRecommendation, deps))

    def fixVersionRecommendations(self, workDir, staticVersion, versionRecommendationFiles):
        if not self.isAssembly():
            setHomeDir = workDir.file(Dirs.sets, self.name)
        else:
            setHomeDir = workDir.file(Dirs.assemblies, self.name)

        if not exists(setHomeDir):
            print("Component set %s hasn't been checked out yet." % (self.name))
            return

        buildConfigDir = join(setHomeDir, 'build')
        if not exists(buildConfigDir):
            mkdir(buildConfigDir)

        scmversion = join(buildConfigDir, 'scmversion')
        if not exists(scmversion):
            mkdir(scmversion)

        with open(join(scmversion, 'static.version'), 'w') as f:
            f.write(staticVersion)

        versionRecommendation = join(buildConfigDir, 'versionRecommendation')
        if not exists(versionRecommendation):
            mkdir(versionRecommendation)

        for deps in self.dependson:
            if exists(join(setHomeDir, deps)):
                copyfile(join(setHomeDir, deps), join(
                    versionRecommendation, deps))

        for deps in self.dependson:
            if deps in versionRecommendationFiles:
                with open(join(
                        versionRecommendation, deps), 'w') as f:
                    f.write(workDir.alias)

    def updateGit(self, workDir):
        if workDir.version not in self.versions:
            return False
        try:
            if not self.isAssembly():
                repo = Repo.init(workDir.file(Dirs.sets, self.name))
            else:
                repo = Repo.init(workDir.file(Dirs.assemblies, self.name))

            if repo.is_dirty():
                return False
            try:
                origin = repo.remote('origin')
            except ValueError:
                print("No origin repository found.")
                return False
            if origin.url != self.git:
                return False
            branch = repo.head.reference.tracking_branch()
            if self.versions[workDir.version] == branch.remote_head:
                origin.pull()
            else:
                print("%s: Mismatching branch configuration exepected '%s' but was '%s'" % (
                    self.name, self.versions[workDir.version], branch.remote_head))

            repo.close()
            return True
        except IOError as error:
            print(error)
            return False

    def getVersionRecommendationName(self):
        return self.versionRecomFileNames

    def addVersionRecommendation(self, assembly, fileName):
        self.versionRecomFileNames.append(fileName)

    def isSupported(self, version):
        return int(version) in self.versions

    def getVersions(self):
        return set(self.versions.keys())

    def __str__(self):
        return "%s(%s)" % (self.name, self.git)
