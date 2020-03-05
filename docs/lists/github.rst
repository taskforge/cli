Github TaskList
===============

Why use the Github list
-----------------------

Configuration
-------------

The Github list takes the following configuration keys:

base_url
++++++++

The base URL to use when making calls to the Github API. Defaults to
``'https://api.github.com'``. You should only need to configure this
when using a Github Enterprise server.

create_repo
+++++++++++

This repo will be used when creating issues in the Github API. It is a
string of the form ``user/repo``. If not set you will not be able to
add issues to a Github TaskList.

query_repo
++++++++++

If provided the list will only show issues from the configured
repo. It is a string of the form ``user/repo``. If not set this list
will query from all issues assigned to the authenticated user.

self_assign_on_create
+++++++++++++++++++++

If ``true`` all issues created to this list will be assigned to the
authenticated user.

use_metadata_labels
+++++++++++++++++++

Taskforge provides some metadata around tasks that Github Issues do
not support, such as priority. When ``use_metadata_labels`` is
``true`` taskforge will store some of this metadata using formatted
labels. This defaults to ``false`` to prevent adding unwanted labels
to projects where you do not have those permissions.

sqlite_cache_file
+++++++++++++++++

The Github list uses a SQLite database to cache issues locally to
speed up all operations as well as provide search features that the
Github API does not support. This configuration should be set to an
absolute path where you would like that file stored. Most users will
be able to leave this as the default value.

access_token
++++++++++++

The Github personal access token used for authenticating with the
API. This is preferred to username and password. Additionally, it is
required if both username and password are not provided.

For instructions on generating a personal access token consult the
official Github documentation.

https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line

username
++++++++

Your Github username, only required if ``access_token`` is not set.

password
++++++++

Your Github password, only required if ``access_token`` is not set.

Example Configuration
---------------------

The minimal configuration required to use the Github list is:

.. code::

   [list.config]
   access_token = 'some_personal_access_token'
