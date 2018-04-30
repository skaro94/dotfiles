import os
import sys
from sys import stderr

sys.path.append('..')

from config import sep_suffix
from config import *

def _wrap_colors(ansicode):
    return (lambda msg: ansicode + str(msg) + '\033[0m')
GRAY   = _wrap_colors("\033[0;37m")
WHITE  = _wrap_colors("\033[1;37m")
RED    = _wrap_colors("\033[0;31m")
GREEN  = _wrap_colors("\033[0;32m")
YELLOW = _wrap_colors("\033[0;33m")
CYAN   = _wrap_colors("\033[0;36m")
BLUE   = _wrap_colors("\033[0;34m")


def log(msg, cr=True):
    stderr.write(msg)
    if cr:
        stderr.write('\n')


def check_not_exist(source, if_log=True):
    # bad entry if source does not exists...
    if not os.path.lexists(source):
        if if_log:
            log(RED("source %s : does not exist" % source))
        return True
    return False


def check_machine_type():
    assert(default_type in machine_type)
    log(YELLOW("what is your machine type? "  + "(" +
        "".join(["{}({})/".format(k, machine_type[k]) for k in machine_type.keys()])[:-1]
        + ")"))
    mtype = raw_input().lower()
    if not (mtype in machine_type):
        log(RED("Invalid option ({}), falling back to {}".format(mtype,
            machine_type(default_type))))
        mtype = default_type

    return machine_type[mtype]


# ~/(task).mtype -> ~/(task).mtype/(mtype)
def get_machine_specific_opts(current_dir, mtype, tasks):
    for target, task_dir in sorted(tasks.items()):
        source = os.path.join(current_dir, os.path.expanduser(task_dir))

        if check_not_exist(source, False):
            mtype_dir = source + sep_suffix
            if not check_not_exist(mtype_dir):
                # in mtype_dir
                chosen_file = ''
                if os.path.isdir(mtype_dir):
                    new_source = os.path.join(mtype_dir, mtype)
                    chosen_file = mtype
                    if check_not_exist(new_source):
                        for (_, _, filename) in os.walk(source):
                            log(RED("Falling back to {}".format(filename)))
                            chosen_file = filename
                            break

                    chosen_file = '/' + chosen_file

                new_task_dir = task_dir + sep_suffix + chosen_file
                tasks[target] = new_task_dir

    return tasks
