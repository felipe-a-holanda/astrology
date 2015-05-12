from os.path import join

from fabric.operations import run
from fabric.api import task
from fabric.state import env
from contextlib import contextmanager
from fabric.api import *


env.user = 'root'
env.http_user = 'www-data'
env.http_group = 'www-data'
env.hosts = ['104.236.42.196']
env.base_path = '/var/www'
env.path = join(env.base_path, 'astrology')
env.venv_name = 'venv'
env.venv = join(env.base_path, env.venv_name)
env.github_repo = 'git@github.com:flp9001/astrology.git'
env.activate = 'source {venv}/bin/activate'.format(**env)


@contextmanager
def virtualenv():
    with cd(env.path):
        with prefix(env.activate):
            yield

@task
def os_dep():
    with cd(env.path):
        run('./install_os_dependencies.sh install')

@task 
def py_dep():
    with virtualenv():
        run("pip install -r {path}/requirements/production.txt".format(**env))

@task
def restart():
    run('service apache2 restart')


@task
def initial_setup():
    run('mkdir -p {base_path}'.format(**env))
    with cd(env.base_path):
        run('git clone {github_repo}'.format(**env))
        run('virtualenv {venv_name}'.format(**env))    
    os_dep()
    py_dep()
    
    


@task
def deploy():
    with cd(env.path):
        run("git pull")
        run("git reset --hard")
        run("git checkout -f")
        run("chown -R {http_user}:{http_group} .".format(**env))
    py_dep()
    restart()

@task
def test():
    
    with cd(env.path):
        run('pwd')
