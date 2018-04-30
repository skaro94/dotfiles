import pkgutil
import subprocess
import os
import sys
import re
from signal import signal, SIGPIPE, SIG_DFL

sys.path.append("..")

from build_utils import get_machine_specific_opts
from config import get_symlinks, contained_nvim


def setup(mtype, current_dir):
    python_config_path = current_dir + '/python'

    python_versions = ['3.6.5', '2.7.14', 'pypy3.5-5.10.0']
    package_list = ['virtualenv', 'virtualenvwrapper']

    pyenv_install = {
        'pyenv_install': ['curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash'],
    }

    def upsert_package(package):
        if not pkgutil.find_loader(package):
            print("installing {}".format(package))
            subprocess.check_call(["python", '-m', 'pip', 'install', package])
        else:
            print("package {} is already installed".format(package))

    def run_dict(pac_dict):
        for key, pac in pac_dict.items():
            for cmd in pac:
                subprocess.call(['bash', '-c', cmd], preexec_fn=lambda: signal(SIGPIPE, SIG_DFL))

    run_dict(pyenv_install)

    process = subprocess.Popen(['pyenv', 'versions', '--bare'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    current_vers = out.decode('utf-8').split('\n')[:-1]
    versions_to_install = list(set(python_versions) - set(current_vers))
    # favor official compilers, specifically ver 3.x
    current_vers = sorted(current_vers, key=lambda x: re.sub(r'[A-Za-z]', '0', x), reverse=True)

    pyenv_dict = {
        'pyenv_init': ['bash {}/pyenv_setup.sh'.format(python_config_path)],
        'pyenv_python': ['pyenv install ' + version for version in versions_to_install],
        'pyenv_global': ['pyenv global ' + current_vers[0]]
    }
    pipsi_dict = {
        'pipsi_pew': ['pipsi install pew'],
        'pipsi_pipenv': ['pipsi install pipenv'],
    }

    requirements = {'~/requirements': 'requirements'}
    requirements = get_machine_specific_opts(python_config_path, mtype, requirements)
    requirement = requirements.keys()[0]
    requirement = os.path.join(python_config_path, os.path.expanduser(requirement))
    print("REQUIREMENTS: ", requirement)

    for pac in package_list:
        upsert_package(pac)

    run_dict(pyenv_dict)

    upsert_package('pipsi')

    run_dict(pipsi_dict)

    # configure nvim python
    if not contained_nvim:
        symlinks = get_symlinks()
        for target, source in symlinks.items():
            subprocess.call(['ln', '-sf', os.path.expanduser(source), os.path.expanduser(target)])
            ppath, pfile = os.path.split(source)
            pnum = re.sub(r"\D", "", pfile)
            pip23 = 'pip' + pnum
            pip_path = os.path.join(ppath, pip23)
            subprocess.call([pip_path, 'install', 'neovim'])
    else:
        pipenv_nvim = True

    # configure pipenv
    current_path = os.getcwd()
    os.chdir(os.path.expanduser('~'))
    subprocess.call(['pipenv', 'shell'])
    if os.path.lexists(requirement):
        subprocess.call(['pipenv', 'install', '-r', requirement])
    os.chdir(current_path)
