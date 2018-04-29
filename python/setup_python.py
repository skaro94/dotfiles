import pip
import pkgutil
import subprocess
import os
from signal import signal, SIGPIPE, SIG_DFL


def setup(mtype, current_dir):
    python_versions = ['3.6.5', '2.7.14', 'pypy3.5-5.10.0']
    package_list = ['virtualenv', 'virtualenvwrapper']
    pyenv_dict = {
        'pyenv_install': ['curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash'],
        'pyenv_python': ['pyenv install ' + version for version in python_versions],
        'pyenv_global': ['pyenv global ' + python_versions[0]]
    }
    pipsi_dict = {
        'pipsi_pew': ['pipsi install pew'],
        'pipsi_pipenv': ['pipsi install pipenv'],
    }

    requirements = 'requirements'
    requirements = os.path.join(current_dir, os.path.expanduser(requirements))
    requirements = requirements if os.path.isfile(requirements) else os.path.join(requirements, mtype)

    def upsert_package(package):
        if not pkgutil.find_loader(package):
            print("installing {}".format(package))
            pip.main(['install', package])
        else:
            print("package {} is already installed".format(package))

    def run_dict(pac_dict):
        for key, pac in pac_dict.items():
            print("installing {}".format(key))
            for cmd in pac:
                subprocess.call(['bash', '-c', cmd], preexec_fn=lambda: signal(SIGPIPE, SIG_DFL))

    for pac in package_list:
        upsert_package(pac)

    run_dict(pyenv_dict)

    upsert_package('pipsi')

    run_dict(pipsi_dict)

    if os.path.lexists(requirements):
        subprocess.call(['pipenv', 'install', '-r', requirements])
