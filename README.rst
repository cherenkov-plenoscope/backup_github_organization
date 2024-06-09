#####################################################
Downloading an entire GitHub organization for backups
#####################################################

This package uses the pyhton package ``github-backup``
to backup an entire GitHub organization.

*******
install
*******

.. code-block::

    pip install github-backup

*****
usage
*****

In order to download and backup all parts of a GitHub organization, even the
private repositories, we use GitHub's tokens for fine-grained access. With the
token we will download and archive the the ogranization on our local machine.
In the end, we might set up a cron job to repeat the backup automatically.


***************************************
Make or update GitHub fine access token
***************************************

A user with access to the organiation creates an access token.

(2024-06-09) Log into GitHub and go to your account settings:

``https://github.com/settings/profile``

Go to:
``Developer settings`` -> ``Personal access tokens`` -> ``Fine-grained tokens``.

Create new token and copy the content to your local machine and store it in a
text file e.g. in:
``/home/USER/.github/fine-grained-access-tokens/my_backup_token.txt``.


**********************
Call ``github-backup``
**********************

Look at the example in ``download_github_organization.py``

.. code-block::

    download_github_organization\
        --token_path\
        /home/USER/.github/fine-grained-access-tokens/my_backup_token.txt\
        --name cherenkov-plenoscope\
        --output_path OUTPUT.TAR.GZ

The script ``download_github_organization`` is just a wrapper which calls
``github-backup`` and further dumps the download into a compressed tape archive
(.tar.gz). Also, it can generate filenames for the backup with timestamps.


********************
Installing a cronjob
********************

To be discussed...
