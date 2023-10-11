from confluence_api_utils import utils
import os

token = os.getenv("API_TOKEN")
user = os.getenv("CONFLUENCE_USER")
url = os.getenv("CONFLUENCE_URL")
token = os.getenv("API_TOKEN")
parent_id = os.getenv("PARENT_ID")
directory = os.getenv("FOLDER")
title = os.getenv("PROJECT_TITLE")


def main():
    confluence = utils.authenticate(url, user, token)
    utils.convert_md_to_html(directory, confluence, parent_id, title)

if __name__ == '__main__':
    main()