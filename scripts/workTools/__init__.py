from __future__ import print_function
from workTools.icm import setup_icm, update_icm, list_icm, add_componentset, build_componentset, utils
from workTools.icm.workdir import Workdir
from os.path import expanduser, join
from os import environ
from subprocess import run, CalledProcessError
from yaml import load
import easyargs
import pkg_resources

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


@easyargs
class WorkTools(object):
    """Work tool collection. JMetzner (at) intershop.de"""

    def __init__(self):
        self.workdir = expanduser('~/work')

    def setup(self, version, _alias, _dbType):
        """
        Setup a new intershop commerce management server
        :param _alias: The short handle that is associated with a wt-dir
        :param version: The ICM marketing version that you associate with this wt-dir
        :param _dbType: The database type to be used (oracle=default or mssql)
        """
        try:
            int(version)
        except ValueError as error:
            print(
                "Versions must be given as integer. E.g 7900 instead of 7.9 or 7.10.19 or...")
            return
        with open(utils.getVersionFile(self.workdir)) as versionMapFile:
            unknownVersion = 0
            supportedVersions = set()
            projects = load(versionMapFile, Loader)
            for project in utils.getProjects(projects.keys(), projects).values():
                if not project.isSupported(version):
                    unknownVersion += 1
                supportedVersions |= project.getVersions()

            if unknownVersion == len(utils.getProjects(projects.keys(), projects)):
                print("Version '%s' is not supported." % (version))
                print("Supported versions are: ", supportedVersions)
                return

        if _dbType != None:
            setup_icm.setup(int(version), _alias or version,
                            self.workdir, _dbType)
        else:
            setup_icm.setup(int(version), _alias or version, self.workdir)
        list_icm.index(self.workdir)

    def list(self):
        """
        List all managed intershop commerce management server(s)
        """
        list_icm.list(self.workdir)

    def update(self, alias):
        """
        Update settings of intershop commerce management server. Not building it!
        :param alias: The short handle that is associated with a wt-dir
        """
        wd = None
        for i in Workdir(self.workdir).list():
            if i.alias == alias:
                wd = i

        if wd == None:
            print("No work directory found with associated alias '%s'." % (alias))
            self.list()
        else:
            update_icm.update(alias, wd, utils.getVersionFile(self.workdir))

    def add(self, alias, project):
        """
        Add multi-project to Intershop commerce management server
        :param alias: The short handle that is associated with a wt-dir
        :param project: The name of the assembly or component set to be added
        """
        wd = None
        for i in Workdir(self.workdir).list():
            if i.alias == alias:
                wd = i

        if wd == None:
            print("No work directory found with associated alias '%s'." % (alias))
            self.list()
        else:
            add_componentset.addComponentset(
                wd, alias, project, utils.getVersionFile(self.workdir))

    def build(self, alias, _project):
        """
        Build and publish the artifact of a multi-project
        :param alias: The short handle that is associated with a wt-dir
        :param _project: The name of the assembly or component set to be build or build all existing
        """
        wd = None
        for i in Workdir(self.workdir).list():
            if i.alias == alias:
                wd = i

        if wd == None:
            print("No work directory found with associated alias '%s'." % (alias))
            self.list()
            return

        if _project != None:
            build_componentset.build(
                wd, alias, _project, utils.getVersionFile(self.workdir))
        else:
            build_componentset.buildAll(
                wd, alias, utils.getVersionFile(self.workdir))

    def version(self):
        """
        Print version information
        """
        print(pkg_resources.get_distribution('WorkTools').version)

    def cd(self, alias, ):
        """
        Change to the work directory associated with the given alias.
        :param alias: The short handle that is associated with a wt-dir
        """
        wd = None
        for i in Workdir(self.workdir).list():
            if i.alias == alias:
                wd = i

        if wd == None:
            print("No work directory found with associated alias '%s'." % (alias))
            self.list()
        else:
            if "SHELL" not in environ:
                print("Cannot change to %s" % wd.wtdir)
            else:
                try:
                    run([environ['SHELL']], cwd=wd.wtdir)
                except CalledProcessError as identifier:
                    pass


if __name__ == '__main__':
    WorkTools()
