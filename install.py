#!/usr/bin/env python
# -*- coding: utf-8 -*-

print('''
   @wookayin's              ███████╗██╗██╗     ███████╗███████╗
   ██████╗  █████╗ ████████╗██╔════╝██║██║     ██╔════╝██╔════╝
   ██╔══██╗██╔══██╗╚══██╔══╝█████╗  ██║██║     █████╗  ███████╗
   ██║  ██║██║  ██║   ██║   ██╔══╝  ██║██║     ██╔══╝  ╚════██║
   ██████╔╝╚█████╔╝   ██║   ██║     ██║███████╗███████╗███████║
   ╚═════╝  ╚═════╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝

   https://dotfiles.wook.kr/
''')

import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f', '--force', action="store_true", default=False,
                    help='If specified, it will override existing symbolic links')
parser.add_argument('--vim-plug', default='update', choices=['update', 'install', 'none'],
                    help='vim plugins: update and install (default), install only, or do nothing')
parser.add_argument('--skip-zplug', action='store_true')
args = parser.parse_args()

################# BEGIN OF FIXME #################

# Task Definition
# (path of target symlink) : (location of source file in the repository)



################# END OF FIXME #################

def _wrap_colors(ansicode):
    return (lambda msg: ansicode + str(msg) + '\033[0m')
GRAY   = _wrap_colors("\033[0;37m")
WHITE  = _wrap_colors("\033[1;37m")
RED    = _wrap_colors("\033[0;31m")
GREEN  = _wrap_colors("\033[0;32m")
YELLOW = _wrap_colors("\033[0;33m")
CYAN   = _wrap_colors("\033[0;36m")
BLUE   = _wrap_colors("\033[0;34m")


import os
import sys
import subprocess

from signal import signal, SIGPIPE, SIG_DFL
from optparse import OptionParser
from sys import stderr

from config import *


def log(msg, cr=True):
    stderr.write(msg)
    if cr:
        stderr.write('\n')


def check_not_exist(source):
    # bad entry if source does not exists...
    if not os.path.lexists(source):
        log(RED("source %s : does not exist" % source))
        return True
    return False


def check_machine_type():
    assert(default_type in machine_type)
    log(YELLOW("what is your machine type? "  + "(" +
        "".join(["{}({})/".format(k, machine_type(k)) for k in machine_type.keys()])[:-1]
        + ")")
    mtype = raw_input().lower()
    if not (mtype in machine_type):
        log(RED("Invalid option ({}), falling back to {}".format(mtype,
            machine_type(default_type))))
        mtype = default_type

    return machine_type(mtype)


# ~/(task) -> ~/(task)/(mtype) if is_dir
def get_machine_specific_opts(mtype, tasks):
    keys = tasks.keys()
    for task_dir in keys:
        source = os.path.join(current_dir, os.path.expanduser(task_dir))

        if check_not_exist(source):
            continue

        if os.path.isdir(source):
            filename = mtype
            new_source = os.path.join(source, filename)
            if check_not_exist(new_source):
                for (_, _, a_filename) in os.walk(source):
                    filename = a_filename
                    new_source = os.path.join(source, filename)
                    log(RED("Falling back to {}".format(filename)
                    break

        new_task_dir = task_dir + '/' + filename

        dest = tasks[task_dir]
        del tasks[task_dir]
        tasks[new_task_dir] = dest

    return tasks


# get current directory (absolute path)
current_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(current_dir)

# check if git submodules are loaded properly
stat = subprocess.check_output("git submodule status --recursive",
                               shell=True, universal_newlines=True)
submodule_issues = [(l.split()[1], l[0]) for l in stat.split('\n') if len(l) and l[0] != ' ']

if submodule_issues:
    stat_messages = {'+': 'needs update', '-': 'not initialized', 'U': 'conflict!'}
    for (submodule_name, submodule_stat) in submodule_issues:
        log(RED("git submodule {name} : {status}".format(
            name=submodule_name,
            status=stat_messages.get(submodule_stat, '(Unknown)'))))
    log(RED(" you may run: $ git submodule update --init --recursive"))

    log("")
    log(YELLOW("Do you want to update submodules? (y/n) "), cr=False)
    shall_we = (raw_input().lower() == 'y')
    if shall_we:
        git_submodule_update_cmd = 'git submodule update --init --recursive'
        # git 2.8+ supports parallel submodule fetching
            if git_version >= '2.8': git_submodule_update_cmd += ' --jobs 8'
        except Exception as e:
            pass
        log("Running: %s" % BLUE(git_submodule_update_cmd))
        subprocess.call(git_submodule_update_cmd, shell=True)
    else:
        log(RED("Aborted."))
        sys.exit(1)

mtype = check_machine_type()
tasks = get_machine_specific_opt(mtype, tasks)

for target, source in sorted(tasks.items()):
    # normalize paths
    source = os.path.join(current_dir, os.path.expanduser(source))
    target = os.path.expanduser(target)

    # if --force option is given, delete and override the previous symlink
    if os.path.lexists(target):
        is_broken_link = os.path.islink(target) and not os.path.exists(os.readlink(target))

        if check_not_exist(source):
            continue

        if args.force or is_broken_link:
            if os.path.islink(target):
                os.unlink(target)
            else:
                log("{:50s} : {}".format(
                    BLUE(target),
                    YELLOW("already exists but not a symbolic link; --force option ignored")
                ))
        else:
            log("{:50s} : {}".format(
                BLUE(target),
                GRAY("already exists, skipped")
            ))

    # make a symbolic link if available
    if not os.path.lexists(target):
        try:
            mkdir_target = os.path.split(target)[0]
            os.makedirs(mkdir_target)
            log(GREEN('Created directory : %s' % mkdir_target))
        except:
            pass
        os.symlink(source, target)
        log("{:50s} : {}".format(
            BLUE(target),
            GREEN("symlink created from '%s'" % source)
        ))

for action in post_actions:
    if not action:
        continue
    log(CYAN('Executing: ') + action.strip().split('\n')[0])
    subprocess.call(['bash', '-c', action],
                    preexec_fn=lambda: signal(SIGPIPE, SIG_DFL))

log("\n" + GREEN("Done! "), cr=False)
log(GRAY("Please restart shell (e.g. `exec zsh`) if necessary\n"))
