import requests
import json

class Tag_suggestion():
    def get_label(query):
        wiki_api = "https://www.wikidata.org/w/api.php"

        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': query
        }

        result = requests.get(wiki_api, params = params)
        suggested_tags = []
        try:

            result_json = result.json()['search']

           

            for item in result_json:
                tag = item.get("id") + ' - ' + item.get("label") + ' - ' + item.get("description")
                suggested_tags.append(tag)
        except:
            pass
        return suggested_tags
