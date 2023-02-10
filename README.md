# zotero2notion
## Description
Add entries from Zotero into a database in Notion

## Setup
- Pull the latest version of the repository
- Create a file named `<NAME>.py` and place it in the folder `keys`. `<NAME>` can be anything; the script will add a tag `<NAME>` to the Notion pages pulled from this library.
- The file '<NAME>.py' should look like
```
# zotero
library_id = 'xxxxxxxxxxxxxx'
library_type = 'xxxx'
api_key = 'xxxxxxxxxxxxxxxxxxxxxxx'

# notion
database_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
notion_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

### To get Zotero API key `api_key`
- Log in to your online Zotero account
- Navigate to `Settings > Feeds/API > Create new private key`
- Make sure that the key has the following access:
  - `Personal Library > Allow library access`
  - `Personal Library > Allow write access`
  - `Default Group Permissions > Read/Write`
- This is your Zotero API key `api_key`

### To get Zotero Library ID
- If it is your personal library, `library_type = 'user'` and `library_id` is your Zotero user ID. 
  - You should be able to find your Zotero user ID in `Settings > Feeds/API`
- If it is a group library, `library_type = 'group'` and `library_id` is the group ID. To get the group ID:
  - Go to the `Groups` tab in your account.
  - Click on the group
  - Look at the URL. The group ID are the numbers following `https://www.zotero.org/groups/`

### To get Notion API
- Log in to `https://www.notion.so/my-integrations`
- Create a new integration token. This is your `notion_token`

### To set up a Notion database
- Create a database with at least the following properties (case sensitive):
  - `Name` as title
  - `Authors` of type `Multi-select`
  - `Tags` of type `Multi-select`
  - `URL` of type `URL`
- Get the database ID:
  - Click on `Share > Copy Link`
  - The link should look like `https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxx?v=yyyyyyyyyyyyyyyyyyyyyyyyyyyy`
  - The `xxxxxxxxxxxxxxxxxxxxxxxxxxxx` part is your `database_id`
- Allow the API token to access the database:
  - On the top-right corner, click on the three dots (to the right of `Share`)
  - Click on `Add connections`
  - Search the name of the integration token you created above. Confirm to give it access to the database.

### To run the script
- Open Terminal
- Navigate to the folder of the script
- Run `python3 main.py`. 
- The script periodically checks Zotero for new entries and add corresponding pages to Notion. Keep it running.  
