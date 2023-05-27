import requests
import toml
import os
import subprocess
from packaging import version

def check_pull_restart(working_dir, gh_raw_url_toml, service_name, local_toml_filename='pyproject.toml'):
    default_dir = os.getcwd()
    
    pyproject_content_gh = requests.get(gh_raw_url_toml).text
    pyproject_content_gh_parsed = toml.loads(pyproject_content_gh)
    gh_version = pyproject_content_gh_parsed['tool']['poetry']['version']
    
    pyproject_content_local_parsed = toml.load(os.path.join(working_dir, local_toml_filename))
    local_version = pyproject_content_local_parsed['tool']['poetry']['version']
    
    if version.parse(gh_version) > version(local_version):
        # change dir
        os.chdir(working_dir)
        # pull 
        subprocess.run(
            'git pull',
            shell=True
        )
        # install new dependencies if any
        subprocess.run(
            'poetry install',
            shell=True
        )
        # restart service
        subprocess.run(
            f'systemctl --user restart {service_name}',
            shell=True
        )
        os.chdir(default_dir)
        
        return True
    else:
        return False

