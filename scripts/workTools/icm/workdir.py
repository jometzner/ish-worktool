from os import mkdir, rmdir, listdir
from os.path import expanduser, join, exists
from yaml import load, dump
import enum
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Workdir(object):

    def __init__(self, workHomeDir, databaseType="oracle"):
        self.workHomeDir = workHomeDir
        self.wtdir = None
        self._count = None
        self.wtid = None
        self.version = None
        self.alias = None
        self.type = "icm"
        self.databaseType = databaseType
        self.subDirs = []

    def list(self):
        ret = []
        data = load(self.wtDirectoryFile(), Loader=Loader)
        for wtid in data:
            if wtid != 'meta':
                wd = Workdir(self.workHomeDir)
                wd.wtid = wtid
                wd.alias, wd.databaseType, wd.type, wd.version = data[wtid].values()

            if exists(join(self.workHomeDir, wtid)):
                wd.subDirs = listdir(join(self.workHomeDir, wtid))
                wd.wtdir = join(self.workHomeDir, wtid)
                wd._count = int(wtid[len('gradle')])
                ret.append(wd)
        return ret

    def beginWT(self, version, alias):
        data = load(self.wtDirectoryFile(), Loader=Loader)
        found = None
        for wts in data:
            if "alias" in data[wts] and data[wts]['alias'] == alias:
                found = wts

        if found != None:
            print("%s is already used by %s" %
                  (alias, join(self.workHome(), found)))
            raise IOError()
        self._count = 1 + data['meta']['count']
        self.wtid = 'gradle' + str(self._count)
        self.wtdir = join(self.workHome(), self.wtid)
        self.version = version

        try:
            if not exists(self.wtdir):
                mkdir(self.wtdir)
        except IOError as error:
            print("Cannot prepare new work dir environment")
            raise error
        return self

    def rollbackWT(self):
        try:
            for subdir in self.subDirs:
                rmdir(join(self.wtdir, subdir))
            if self.wtdir != None:
                rmdir(self.wtdir)
        except IOError as error:
            print(error)

    def addDir(self, name):
        try:
            if not exists(join(self.wtdir, name)):
                mkdir(join(self.wtdir, name))
            self.subDirs.append(name)
        except IOError as error:
            print("Cannot add %s to wt-dir %s" % (name, self.wtdir))
            raise error
        return self

    def commitWT(self, version, alias):
        data = load(self.wtDirectoryFile(), Loader=Loader)
        data['meta']['count'] = self._count
        data[self.wtid] = {'alias': alias, 'version': version,
                           'type': 'icm', 'databaseType': self.databaseType}
        dump(data, self.wtDirectoryFile('w'), Dumper=Dumper)

    def wtDirectoryFile(self, mode='r'):
        f = join(self.workHome(), '.workToolDir')
        try:
            if exists(f):
                return open(f, mode)
            else:
                data = {'meta': {'count': 0}}
                dump(data, open(f, 'a'), Dumper)
                return open(f, mode)
        except IOError as error:
            print(error)

    def workHome(self):
        return self.workHomeDir

    def workingDir(self):
        return self.wtdir

    def port(self, base=0):
        id = int(self.wtid[len('gradle')])
        return int(base) + id - 1

    def file(self, wttype, name):
        return join(self.wtdir, wttype.name, name)

    def context(self):
        ret = {}
        for dir in self.subDirs:
            ret[dir] = join(self.workingDir(), dir)
        return ret


class Dirs(enum.IntEnum):
    developer = 1
    assemblies = 2
    server = 3
    sets = 4
    gradle = 5
