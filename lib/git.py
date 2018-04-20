import subprocess
import os


def get_commit_id():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])[:6]


def update_version():
    version_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'version.py')

    try:
        git_commit = get_commit_id()
    except subprocess.CalledProcessError():
        return

    with open(version_file_path) as version_file:
        version_lines = version_file.readlines()

    with open(version_file_path, 'w+') as version_file:
        for line in version_lines:
            if line.startswith('GIT_COMMIT'):
                try:
                    line = 'GIT_COMMIT = "' + git_commit.decode('ascii') + '"\n'
                except:
                    pass
            version_file.write(line)
