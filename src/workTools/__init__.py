from __future__ import print_function
from workTools.icm import setup_icm, update_icm, list_icm, add_componentset, build_componentset, utils
from workTools.icm.workdir import Workdir
from os.path import expanduser, join
from os import environ
from subprocess import run, CalledProcessError
from yaml import load
import argparse
import pkg_resources

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


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
        try:
            version = pkg_resources.get_distribution('ISHWorkTools').version
            print(f"ISHWorkTools version: {version}")
        except pkg_resources.DistributionNotFound:
            print("ISHWorkTools package is not installed.")

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

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Work tool collection')
        subparsers = parser.add_subparsers(dest='command')

        setup_parser = subparsers.add_parser('setup', help='Setup a new intershop commerce management server')
        setup_parser.add_argument('version', type=str, help='The ICM marketing version')
        setup_parser.add_argument('_alias', type=str, help='The short handle associated with a wt-dir')
        setup_parser.add_argument('_dbType', type=str, choices=['oracle', 'mssql'], default='oracle', help='The database type to be used')

        list_parser = subparsers.add_parser('list', help='List all managed intershop commerce management server(s)')

        update_parser = subparsers.add_parser('update', help='Update settings of intershop commerce management server')
        update_parser.add_argument('alias', type=str, help='The short handle associated with a wt-dir')
        
        build_parser = subparsers.add_parser('build', help='Build and publish the artifact of a multi-project')
        build_parser.add_argument('alias', type=str, help='The short handle associated with a wt-dir')

        subparsers.add_parser('version', help='Print version information')

        cd_parser = subparsers.add_parser('cd', help='Change to the work directory associated with the given alias')
        cd_parser.add_argument('alias', type=str, help='The short handle associated with a wt-dir')
        

        args = parser.parse_args()
        return args

    def run(self):
        args = self.parse_args()
        if args.command == 'setup':
            self.setup(args.version, args._alias, args._dbType)
        elif args.command == 'list':
            self.list()
        elif args.command == 'update':
            self.update(args.alias)
        elif args.command == 'build':
            self.build(args.alias, None)
        elif args.command == 'version':
            self.version()
        elif args.command == 'cd':
            self.cd(args.alias)
        else:
            return -1
