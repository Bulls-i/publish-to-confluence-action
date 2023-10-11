from atlassian import Confluence
from requests.exceptions import HTTPError
import markdown
import os
from fnmatch import fnmatch


def authenticate(jira_url: str, jira_username: str, jira_api_token: str):
    """
    This functions authenticates an user to jira.

    Parameters:
    - `jira_url`: The URL of your Confluence instance, used for API calls and publishing content.
    - `jira_username`: Your Atlassian account's username, required for authentication when interacting with Confluence.
    - `jira_api_token`: An API token generated for your Atlassian account, used for authentication when making API calls to Confluence

    Returns:
    - `confluence_auth`: Confluence object. See https://atlassian-python-api.readthedocs.io/confluence.html

    """
    confluence_auth = Confluence(
        url=jira_url, username=jira_username, password=jira_api_token, cloud=True
    )
    print("Authenticated successfully")
    return confluence_auth


def _try_creating_or_updating_page(
    confluence_auth: Confluence, parent_id, space_id, title, body
):
    """
    This function tries to create a new page or update an existing page.

    Parameters:
    - `confluence_auth`: Confluence object. See https://atlassian-python-api.readthedocs.io/confluence.html
    - `parent_id`: The id of the page who will be the parent for the new page.
    - `space_id`: The id of the space where the page will be created.
    - `title`: The title of the new page.
    - `body`: The content of the new page.


    Returns:
    - `None`
    """
    try:
        if confluence_auth.page_exists(space_id, title):
            page_id = confluence_auth.get_page_id(space_id, title)
            confluence_auth.update_existing_page(page_id, title, body)
            print("Updated page successfully")
        else:
            confluence_auth.create_page(space_id, title, body, parent_id)
            print("Created page successfully")
    except HTTPError:
        print(
            "incoming request is incomplete or otherwise invalid. For example an incorrect parent id."
        )


def _create_parent_page(
    confluence_auth: Confluence, parent_id: int, space_id: str, title: str
):
    """
    This function creates a new parent page.
    All other pages will be created in this parent page.

    Parameters:
    - `confluence_auth`: Confluence object. See https://atlassian-python-api.readthedocs.io/confluence.html
    - `parent_id`: The id of the page who will be the parent for the new page.
    - `space_id`: The id of the space where the page will be created.
    - `title`: The title of the new page.

    Returns:
    - `parent_page_id`; The id of the created page.
    """
    try:
        if confluence_auth.page_exists(space_id, title):
            print("Parent page already exists for this project")
        else:
            confluence_auth.create_page(space_id, title, "", parent_id)
            print("Created parent page successfully")
    except HTTPError:
        print(
            "incoming request is incomplete or otherwise invalid. For example an incorrect parent id."
        )
    parent_page_id = confluence_auth.get_page_id(space_id, title)
    return parent_page_id


def publish_pages_and_convert_md_to_html(directory: str, confluence_auth: Confluence, parent_id: str, title: str):
    """
    This function converts all found markdown pages.
    Then publishes all those files to confluence.

    Parameters:
    - `directory`: The directory containing the files. This will get checked recursively 
    - `confluence_auth`: Confluence object. See https://atlassian-python-api.readthedocs.io/confluence.html
    - `parent_id`: The id of the page who will be the parent for the new page.
    - `title`: The title of the new page.

    Returns:
    - `None`    
    """

    space_id = confluence_auth.get_page_space(parent_id)
    parent_id = _create_parent_page(confluence_auth, parent_id, space_id, title)
    pattern = "*.md"

    for path, subdirs, files in os.walk(directory):
        if path is not directory:
            title = f"{title}/{os.path.basename(path)}"
            _try_creating_or_updating_page(
                confluence_auth, parent_id, space_id, title, ""
            )
            new_parent_id = confluence_auth.get_page_id(space_id, title)
            parent_id = new_parent_id
        for name in files:
            if fnmatch(name, pattern):
                md = os.path.join(path, name)
                with open(f"{md}", "r") as f:
                    text = f.read()
                    html = markdown.markdown(text)
                _try_creating_or_updating_page(
                    confluence_auth,
                    parent_id,
                    space_id,
                    f"{title}_{name[:-3]}",
                    html,
                )
