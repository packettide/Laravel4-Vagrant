from fabric.api import *
from fabric.operations import prompt
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from os import getcwd, path

def vagrant():
    env.hosts = ['vagrant@127.0.0.1:2201']
    env.password = 'vagrant'

def artisan(command):
    with cd('/var/www'):
        run('php artisan ' + command)

def composer(command='update'):
    with cd('/var/www'):
        run('composer ' + command)

def updateComposer():
    sudo('composer self-update')

def setProject(project):
    backupDb()
    local('vagrant halt')
    pFile = open("project", "w")
    pFile.write(project)
    pFile.close()
    local('vagrant up')
    restoreDb()
    composer('update')

def backupDb():
    pFile = open("project", "r")
    project = pFile.read()
    pFile.close()
    sudo('mysqldump -u root database  > /%s.sql' % project)

def restoreDb():
    pFile = open("project", "r")
    project = pFile.read()
    pFile.close()
    if(exists('/%s.sql' % project)):
        sudo('mysql -u root database < /%s.sql' % project)

