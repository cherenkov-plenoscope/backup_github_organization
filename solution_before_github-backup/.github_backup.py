"""
COPYRIGHT 2019, Sebastian A. Mueller

Usage
-----
    github_backup.py <organization_name> <path_with_datetime_template>.tar

Arguments
---------
    argv[1]         Name of your organization on GitHub.

Description
-----------
    Backup a full organization from GitHub
    Uses github's access-tokens to read private repositories.
    Uses git clone --mirror to copy all branches.
    Bundles organization into tape-archive .tar.
"""
from os import path as op
import os
import subprocess
import tempfile
import json
import tarfile
import shutil
import sys
import datetime


now = datetime.datetime.now()
assert len(sys.argv) == 3
organization_name = sys.argv[1]
print("===================================================")
backup_dir = sys.argv[2]
output_filename = "{:s}_{:s}.tar".format(
    now.strftime("%Y-%m-%d_%H-%M-%S"),
    organization_name)
output_path = op.join(backup_dir, output_filename)
output_path = op.abspath(output_path)
print(output_path, flush=True)

output_already_exists = op.exists(output_path)
assert not output_already_exists
assert op.exists(op.dirname(output_path))
assert op.splitext(output_path)[-1] == ".tar"

with open(op.join(op.expanduser("~"), ".github_token.json"), "rt") as f:
    github = json.loads(f.read())
GITHUB_URL_TEMPLATE = "https://api.github.com/orgs/{:s}/repos?per_page=200"
with tempfile.TemporaryDirectory(prefix="download_github_") as tmp_dir:
    org_dict_path = op.join(tmp_dir, "{:s}.json".format(organization_name))
    with open(org_dict_path, "wt") as f:
        curl_rc = subprocess.call([
            "curl",
            "--user",
            "{username:s}:{token:s}".format(
                username=github["username"],
                token=github["token"]),
            "--silent",
            GITHUB_URL_TEMPLATE.format(organization_name)],
            stdout=f)
    with open(org_dict_path, "rt") as f:
        organization = json.loads(f.read())
    assert len(organization) > 0
    tmp_backup_dir = op.join(tmp_dir, organization_name)
    os.makedirs(tmp_backup_dir, exist_ok=True)
    for repository in organization:
        subprocess.call(
            ["git", "clone", "--mirror", repository["ssh_url"]],
            cwd=tmp_backup_dir)
    tmp_archive_path = op.join(tmp_dir, organization_name+".tar")
    with tarfile.open(tmp_archive_path, "w") as tar:
        tar.add(tmp_backup_dir, arcname=organization_name)
    shutil.move(tmp_archive_path, output_path)
