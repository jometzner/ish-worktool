import jinja2 as template
from os import mkdir, rmdir, listdir, remove, name
from os.path import expanduser, join, exists
from workTools.icm.workdir import Workdir, Dirs
from workTools.icm.utils import isLinux
from getpass import getuser
from socket import gethostname


def setup(version, alias, workdir, databaseType="oracle"):
    wt = Workdir(workdir, databaseType)
    try:
        wt.beginWT(version, alias)
        for dir in Dirs:
            wt.addDir(dir.name)

        env = template.Environment(
            loader=template.FileSystemLoader([
                join(workdir, '.dotfiles', 'gradle'),
                join(workdir, '.dotfiles', 'docker')])
        )
        env.globals = {'host': gethostname(),
                       'instanceId': wt._count,
                       'user': getuser(),
                       'alias': alias,
                       'wtdir': wt.wtdir,
                       'wtid': wt.wtid,
                       'os': name,
                       'workdir': workdir}

        generateDeveloper(wt, 'development.properties',
                              env.get_template('development.j2'))
        generateDeveloper(wt, 'environment.properties', env.get_template(
            'environment.j2'), {'licenseFile': lf(workdir), 'databaseType': wt.databaseType})
        generateGradle(wt, 'gradle.properties',
                       env.get_template('gradle.j2'), wt.context())
        generate(join(wt.wtdir, '.envrc'),
                 env.get_template('envrc.j2'))
        generate(join(wt.wtdir, 'docker-compose.yml'),
                 env.get_template('docker-compose.yml.j2'))
        wt.commitWT(version, alias)
        print(alias)
    except IOError as error:
        print("Error: ", error)
        if wt.workingDir() != None:
            for files in listdir(wt.file(Dirs.developer, '')):
                remove(join(wt.wtdir, 'developer', files))
            if exists(join(expanduser('~/.dotfiles'), 'zsh', alias + '.zsh')):
                remove(join(expanduser('~/.dotfiles'), 'zsh', alias + '.zsh'))
            if exists(wt.file(Dirs.gradle, 'gradle.properties')):
                remove(wt.file(Dirs.gradle, 'gradle.properties'))

        wt.rollbackWT()


def lf(workdir):
    path = join(workdir, '.dotfiles', 'license', 'license.xml')
    if exists(path):
        return path
    else:
        print("No license file found under %s" % (path))
        raise IOError()


def generateDeveloper(wt, file, jinjaTemplate, dict={}):
    generate(wt.file(Dirs.developer, file), jinjaTemplate, dict)


def generateGradle(wt, file, jinjaTemplate, dict={}):
    generate(wt.file(Dirs.gradle, file), jinjaTemplate, dict)


def generate(targetFile, jinjaTemplate, dict={}):
    if not exists(targetFile):
        jinjaTemplate.stream(dict).dump(open(targetFile, 'w'))
