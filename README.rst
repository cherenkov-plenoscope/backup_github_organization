#####################################################
Downloading an entire GitHub organization for backups
#####################################################

This package uses the pyhton package 'github-backup'
to backup an entire GitHub organization.

*******
install
*******

.. code-block::

    pip install github-backup

*****
usage
*****

In order to download and backup all parts of a GitHub
organization, even the private repositories, we use
GitHub's tokens for fine access.

.. code-block::

    github-backup
        --token-fine GITHUB_FINE_ACCESS_TOKEN
        --prefer-ssh
        --organization
        --repositories
        --bare
        --private
        --output-directory
        OUTPUT_DIRECTORY
        NAME_OF_GITHUB_ORGANIZATION

