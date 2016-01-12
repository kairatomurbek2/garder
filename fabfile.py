from __future__ import with_statement
from fabric.api import *


def demo_env():
    env.hosts = ['bfp-services.ltestl.com']
    env.port = '51423'
    env.user = 'itattractor'
    env.password = 'rjvg34M.nth#$'
    env.project_path = '/home/itattractor/bigsurvey'


def production_env():
    env.hosts = ['192.241.215.140']
    env.port = '51423'
    env.user = 'bigsurvey'
    env.password = 'XDMVMktKsFdDpxD'
    env.project_path = '/home/bigsurvey/projects/bigsurvey'


def test_production_env():
    env.hosts = ['172.29.22.1']
    env.user = 'bigsurvey'
    env.password = 'bigsurvey'
    env.project_path = '/home/bigsurvey/projects/bigsurvey'
    env.db_name = 'bigsurvey'
    env.db_user = 'bigsurvey_user'
    env.db_password = 'B5S51fZtjWu8Nwa'
    env.backups_dir = '/home/bigsurvey/backups'


def check_env_parameters():
    if not env.get('hosts'):
        raise Exception('Env parameters are not set')


def backup():
    backup_db()
    backup_codebase()


def backup_db():
    user = env.get('db_user')
    db_password = env.get('db_password')
    db_name = env.get('db_name')
    backups_dir = env.get('backups_dir')
    command = 'mysqldump -u{0} -p{1} {2} > {3}/prod-`date +%d-%m-%Y`.sql'.format(
        user, db_password, db_name, backups_dir)
    run(command)


def backup_codebase():
    backups_dir = env.get('backups_dir')
    tarname = 'prod-code-`date +%d-%m-%Y`.tar.gz'
    compress_path = env.get('project_path')
    command = 'tar zcf {0}/{1} -C {2} .'.format(
        backups_dir, tarname, compress_path)
    run(command)


def fetch_from_git(commit):
    run('git fetch')
    run('git fetch --tags')
    run('git stash')
    run('git checkout %s' % commit)


def reload_server():
    sudo('service apache2 reload')


def deploy_demo(commit="master"):
    check_env_parameters()
    with cd(env.get('project_path')):
        fetch_from_git(commit)
        run('./install.sh')
        reload_server()


def deploy_production(commit="master"):
    check_env_parameters()
    with cd(env.get('project_path')):
        fetch_from_git(commit)
        run('./install_prod.sh')
        reload_server()


def deploy_to_test_production(commit="master"):
    check_env_parameters()
    with cd(env.get('project_path')):
        backup()
        fetch_from_git(commit)
        run('./install_prod.sh')
        reload_server()
