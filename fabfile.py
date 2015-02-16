from __future__ import with_statement
from fabric.api import *


def demo_env():
    env.hosts = ['bfp-services.ltestl.com']
    env.user = 'itattractor'
    env.password = 'rjvg34M.nth#$'
    env.port = '51423'
    env.project_path = '/home/itattractor/bigsurvey'


def check_env_parameters():
    if not env.get('hosts'):
        raise Exception('Env parameters are not set')


def deploy():
    check_env_parameters()
    with cd(env.get('project_path')):
        run('git pull')
        run('./install.sh')
        sudo('service apache2 reload')