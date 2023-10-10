from confluence_api_utils import utils
import dotenv
import os

dotenv.load_dotenv()

token = os.getenv("API_TOKEN")
user = os.getenv("CONFLUENCE_USER")
url = os.getenv("CONFLUENCE_URL")
directory = os.getenv("FOLDER")
parent_id = os.getenv("PARENT_ID")


def main():
    confluence = utils.authenticate(url, user, token)
    utils.convert_md_to_html(directory, confluence, parent_id)

if __name__ == '__main__':
    main()