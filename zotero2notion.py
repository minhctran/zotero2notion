from pyzotero import zotero
# import keys
import json
import requests
import importlib
import os
import sys



def creators_to_authors(creators):
	authors = []
	for creator in creators:
		try:
			author = {"name":creator['firstName'] + " " + creator['lastName']}
		except:
			author = {"name":"unknown"}
		authors.append(author)
	return authors

def print_response(response):
	text = response.text

	js = json.loads(text)

	text = json.dumps(js,indent = 4)
	text = "\n ".join(text.split("\\n"))
	if js["object"] == "error":
			print(text)

def create_page(title,creators,paper_url,tags,database_id,notion_token):
	page_id = get_page_from_title(title,database_id,notion_token)
	if page_id != "":
		# if a page with the same name already exists --> just update tags
		print("There is an existing page. Updating tags...")
		for tag in tags:
			add_tag_to_notion_page(page_id,notion_token,tag["name"])
	else:
		# if existing page
		authors = creators_to_authors(creators)
		body = {
			"parent" : {
		        "type": "database_id",
		        "database_id": database_id
		  	},
			"properties" : {
				'Name': {
					'type': 'title', 
					'title': [{
						'type': 'text', 
						'text': {'content': title}
						}]
				},
				'Authors': {
					'type': 'multi_select', 
					'multi_select': authors
				},
				'Tags': {
					'type': 'multi_select', 
					'multi_select': tags
				},
				'URL': {
					'type': 'url', 
					'url': paper_url}
			}
		}
		## create page
		url_page = "https://api.notion.com/v1/pages"
		headers = get_headers(notion_token)

		response = requests.post(url_page, headers=headers,json = body)

		print_response(response)

	return 1

def get_page_from_title(title,database_id,notion_token):
	url_page = "https://api.notion.com/v1/databases/" + database_id + "/query"
	headers = get_headers(notion_token)

	title_filter = { "property" : "Name",
				"title": { "equals" : title}
	}

	body = {
		"filter" : title_filter,
		"page_size" : 1
	}

	response = requests.post(url_page, headers=headers,json = body)
	print_response(response)
	try:
		results = json.loads(response.text)
		results = results["results"]
		page_id = results[0]["id"]
		# print(results[0])
	except:
		print("Page with title \"%s\" not found" % title)
		page_id = ""
		# print("\n    ".join(response.text.split("\\n")))
	return page_id

def add_tag_to_notion_page(page_id,notion_token,tag):
	# pull existing tags
	url_page = "https://api.notion.com/v1/pages/" + page_id
	headers = get_headers(notion_token)
	response = requests.get(url_page, headers=headers)
	tags = json.loads(response.text)
	tags = tags["properties"]["Tags"]["multi_select"]
	# add new_tag to tags
	new_tag = {"name" : tag}
	if new_tag not in tags:
		tags.append(new_tag)
	# update the page
	body = {
		"properties":
			{'Tags': {
				'type': 'multi_select', 
				'multi_select': tags
				}
			}
	}
	response = requests.patch(url_page, headers=headers,json = body)
	print_response(response)
	# print(response.text)


def scan_zotero(filename,library_id,library_type,api_key,database_id,notion_token):
	tags = [{"name":filename}]
	zot = zotero.Zotero(library_id,library_type,api_key)
	zotero_tag = "Noterized " + filename
	items = zot.top(limit=100,tag="-" + zotero_tag)
	# print(items)
	for item in items:
		print('--- Item Type: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))
		# print(item['data']['tags'])
		if item['data']['itemType'] != "attachment":
			title = item['data']['title']
			creators = item['data']['creators']
			paper_url = item['data']['url']
			if len(paper_url) < 2:
				paper_url = 'null'
			print(title)
			create_page(title,creators,paper_url,tags,database_id,notion_token)
			zot.add_tags(item,zotero_tag)
		else:
			zot.add_tags(item,zotero_tag)

def get_headers(notion_token):
	headers = {
		"Authorization": notion_token,
	    "accept": "application/json",
	    "Notion-Version": "2022-06-28",
	    "content-type": "application/json"
	}
	return headers
	
def execute():
	folder_path = os.path.dirname(os.path.realpath(__file__)) + "/"
	folder = "keys"
	folder_full = folder_path + folder
	# print(folder_full)
	file_list = os.listdir(folder_full)
	# print(file_list)
	for file in file_list:

		try:
			filename = os.path.splitext(file)[0]
			ext = os.path.splitext(file)[1]
			if ext == ".py":
				keys = importlib.import_module(folder + "." + filename)
				library_id = keys.library_id
				library_type = keys.library_type
				api_key = keys.api_key
				database_id = keys.database_id
				notion_token = keys.notion_token

				is_key = True
			else:
				is_key = False
		except:
			print(file + " does not contain a key!")
			is_key = False
		if is_key:
			print("------ Scanning " + filename + " ...")
			scan_zotero(filename,library_id,library_type,api_key,database_id,notion_token)

