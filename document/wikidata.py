import requests

class tag_suggestion():
    def get_label(query):
        wiki_api = "https://www.wikidata.org/w/api.php"

        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': query
        }

        result = requests.get(wiki_api, params = params)

        result_json = result.json()['search']

        suggested_tags = []

        for item in a:
            tag = [item.get("id") + ' - ' + item.get("label") + ' - ' + item.get("description")]
            suggested_tags.append(tag)
