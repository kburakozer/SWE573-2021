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


# class Tag_suggestion():
#     def get_label(query):
#         wiki_api = "https://www.wikidata.org/w/api.php"

#         params = {
#             'action': 'wbsearchentities',
#             'format': 'json',
#             'language': 'en',
#             'search': query
#         }

#         result = requests.get(wiki_api, params = params)
#         suggested_tags = []


#         #result_json = result.json()['search']
#         result_json = json.loads(result.text)
#         print(result_json)
#         result_json = json.loads(result.text)['search']
        

#         for item in result_json:
#             tag = item.get("id") + ' - ' + item.get("label") + ' - ' + item.get("description")
#             suggested_tags.append(tag)

#         return suggested_tags




# class Tag_suggestion():
#     def get_label(query):
#         print(query)
#         url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search=" + query + "&language=en"
#         payload = {}
#         headers = {}
#         result = requests.get(url, headers=headers, data=payload)
#         suggested_tags = []

#         print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
#         #result_json = result.json()['search']
#         result_json = json.loads(result.text)
#         print(result_json)
#         result_json = json.loads(result.text)['search']
        

#         for item in result_json:
#             tag = item.get("id") + ' - ' + item.get("label") + ' - ' + item.get("description")
#             suggested_tags.append(tag)

#         return suggested_tags