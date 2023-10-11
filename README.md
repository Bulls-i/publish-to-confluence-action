# Publish to confluence action
This action searches for markdown files in a folder.

These files will be pushed to confluence as pages.

```
name: Publish to Confluence
on:
  pull_request:
    types:
      - closed
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Publish Markdown to Confluence
        uses: Bulls-i/publish-to-confluence-action@v1
        with:
          confluence_url: ${{ secrets.CONFLUENCE_URL }}
          parent_id: ${{ secrets.PARENT_ID }}
          confuence_user: ${{ secrets.ATLASSIAN_USERNAME }}
          api_token: ${{ secrets.ATLASSIAN_API_TOKEN }}
          folder: put the name of the folder containing the files here. 
          For example documentation or info/documentation
          project_title: This will be appended to each file to make sure page names are unique.
```
# Code Of Conduct

[Code of Conduct](documentation/CodeOfConduct.md)