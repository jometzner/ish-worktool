import re
import sys
from workTools import WorkTools
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    work_tools = WorkTools()
    sys.exit(work_tools.run())

