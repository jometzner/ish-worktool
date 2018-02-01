from workTools.icm.workdir import Workdir
from os.path import join
from getpass import getuser
from socket import gethostname

import jinja2 as template


def list(workdir):
    index(workdir)
    for wt in Workdir(workdir).list():
        print("%s, dir=%s, version=%s, " % (wt.alias, wt.wtdir, wt.version))
        pass


def index(workdir):
    env = template.Environment(
        loader=template.FileSystemLoader(join(workdir, '.dotfiles', 'gradle')),
        autoescape=template.select_autoescape(['html'])
    )
    env.globals = {'host': gethostname(),
                   'user': getuser()}

    indexhtml = env.get_template('index.j2')
    indexhtml.stream(workdirs=Workdir(workdir).list()).dump(
        open(join(workdir, 'index.html'), 'w'))
