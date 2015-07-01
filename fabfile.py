from __future__ import with_statement
from fabric.api import *


def demo_env():
    env.hosts = ['bfp-services.ltestl.com']
    env.user = 'itattractor'
    env.password = 'rjvg34M.nth#$'
    env.port = '51423'
    env.project_path = '/home/itattractor/bigsurvey'


def production_env():
    env.hosts = ['192.241.215.140']
    env.user = 'bigsurvey'
    env.password = 'XDMVMktKsFdDpxD'
    env.project_path = '/home/bigsurvey/projects/bigsurvey'


def check_env_parameters():
    if not env.get('hosts'):
        raise Exception('Env parameters are not set')


def fetch_from_git(commit):
    run('git fetch')
    run('git fetch --tags')
    run('git stash')
    run('git checkout %s' % commit)


def reload_server():
    sudo('service apache2 reload')


def create_lettertypes_for_existing_pws():
    run('source virtualenv/bin/activate')
    run('bigsurvey/manage.py create_lettertypes_for_pws')
    run('deactivate')


def deploy_demo(commit="master"):
    check_env_parameters()
    with cd(env.get('project_path')):
        fetch_from_git(commit)
        run('./install.sh')
        # create_lettertypes_for_existing_pws()
        reload_server()


def deploy_production(commit="master"):
    check_env_parameters()
    with cd(env.get('project_path')):
        fetch_from_git(commit)
        run('./install_prod.sh')
        # create_lettertypes_for_existing_pws()
        reload_server()