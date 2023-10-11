from atlassian import Confluence
from requests.exceptions import HTTPError
import markdown
import os
from fnmatch import fnmatch


def authenticate(jira_url, jira_username, jira_api_token):
    confluence_auth = Confluence(
        url=jira_url, username=jira_username, password=jira_api_token, cloud=True
    )
    print("Authenticated successfully")
    return confluence_auth


def try_creating_page(confluence_auth: Confluence, parent_id, space_id, title, body):
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


def convert_md_to_html(directory, confluence_auth: Confluence, parent_id):
    project_title = confluence_auth.get_page_by_id(parent_id)
    space_id = confluence_auth.get_page_space(parent_id)
    pattern = "*.md"

    for path, subdirs, files in os.walk(directory):
        if path is not directory:
            title = f"{project_title['title']}_{path.partition(directory)[-1]}"
            try_creating_page(confluence_auth, parent_id, space_id, title, "")
            new_parent_id = confluence_auth.get_page_id(space_id, title)
            parent_id = new_parent_id
        for name in files:
            if fnmatch(name, pattern):
                md = os.path.join(path, name)
                with open(f"{md}", "r") as f:
                    text = f.read()
                    html = markdown.markdown(text)

                with open(f"{md[:-3] }.html", "w") as f:
                    f.write(html)
                    try_creating_page(
                        confluence_auth,
                        parent_id,
                        space_id,
                        f"{project_title['title']}_{name[:-3]}",
                        html,
                    )
