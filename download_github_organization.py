#!/usr/bin/python
import os
import argparse
import subprocess
import tempfile
import datetime

parser = argparse.ArgumentParser(
    prog="download_github_organization",
    description=(
        "Download an entire GitHub organization and write it into a "
        "tape archive (.tar.gz)."
    ),
)
parser.add_argument(
    "-t",
    "--token_path",
    metavar="TOKEN_PATH",
    type=str,
    help=("Path to a textfile containing your fine access token for GitHub."),
)
parser.add_argument(
    "-n",
    "--name",
    metavar="ORGANIZATION_NAME",
    type=str,
    help=("Name of the organization on GitHub."),
)
parser.add_argument(
    "-d",
    "--output_dir",
    metavar="OUTPUT_DIRECTORY",
    type=str,
    default=None,
    required=False,
    help="Directory where to write the output tar.gz.",
)
parser.add_argument(
    "-o",
    "--output_basename",
    metavar="OUTPUT_BASENAME",
    type=str,
    default=None,
    required=False,
    help=(
        "Path where to write the output tar.gz. "
        "If not given, the output will be written to the current directory "
        "and the filename will be a timestamp plus the name of the "
        "organization."
    ),
)

args = parser.parse_args()

github_fine_acess_token_path = args.token_path
name_of_github_organization = args.name
output_basename = args.output_basename
output_dir = args.output_dir

if output_basename is None:
    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    timestamp = timestamp.replace(":", "-")  # needs to be a valid filename.
    output_basename = "{:s}_{:s}.tar.gz".format(
        timestamp, name_of_github_organization
    )

if output_dir is None:
    output_dir = os.curdir

output_path = os.path.join(output_dir, output_basename)

if os.path.exists(output_path):
    raise RuntimeError("The output path '{:s}' already exists.")

with open(github_fine_acess_token_path, "rt") as f:
    github_fine_acess_token = f.read()
    github_fine_acess_token = str.strip(github_fine_acess_token)  # no newline

with tempfile.TemporaryDirectory(prefix="github-backup-") as tmp:
    github_organization_dir = os.path.join(tmp, name_of_github_organization)
    gitbackcmd = [
        "github-backup",
        "--token-fine",
        github_fine_acess_token,
        "--prefer-ssh",
        "--organization",
        "--repositories",
        "--bare",
        "--private",
        "--output-directory",
        github_organization_dir,
        name_of_github_organization,
    ]
    rc = subprocess.call(gitbackcmd)
    assert rc == 0, "Expected github-backup to return 0. Backup failed"

    github_organization_tar_gz = github_organization_dir + ".tar.gz"
    tarcmd = [
        "tar",
        "--create",
        "--verbose",
        "--gzip",
        "--file",
        github_organization_tar_gz + ".part",
        "--directory",
        github_organization_dir,
        ".",
    ]
    subprocess.call(tarcmd)
    os.rename(github_organization_tar_gz + ".part", github_organization_tar_gz)

    rsynccmd = [
        "rsync",
        "--archive",
        "--verbose",
        "--progress",
        github_organization_tar_gz,
        output_path,
    ]
    subprocess.call(rsynccmd)
