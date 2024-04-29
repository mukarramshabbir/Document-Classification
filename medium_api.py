import pandas as pd
import requests
from data_processing import get_attributes, validity_condition
from html_parser import get_apollo_state

class MediumAPI:
    def __init__(self, headers):
        self.headers = headers

    def search_posts(self, keyword, graph_query, results_limit=50, max_pages=10):
        results = []
        results_file = f"{keyword}_attribute.csv"
        url = 'https://medium.com/_/graphql'
        graph_query = open('searchquery.qu', 'r').read()
        results_limit = 50
        page = 0
        while page <= 10:
            page += 1
            json_data = [
                {
                    'operationName': 'SearchQuery',
                    'variables': {
                        'query': keyword,
                        'pagingOptions': {
                            'limit': results_limit,
                            'page': page,
                        },
                        'withUsers': False,
                        'withTags': False,
                        'withPosts': True,
                        'withCollections': False,
                        'withLists': False,
                        'peopleSearchOptions': {
                            'filters': 'highQualityUser:true OR writtenByHighQulityUser:true',
                            'numericFilters': 'peopleType!=2',
                            'clickAnalytics': True,
                            'analyticsTags': [
                                'web-main-content',
                            ],
                        },
                        'postsSearchOptions': {
                            'filters': 'writtenByHighQualityUser:true',
                            'clickAnalytics': True,
                            'analyticsTags': [
                                'web-main-content',
                            ],
                        },
                        'publicationsSearchOptions': {
                            'clickAnalytics': True,
                            'analyticsTags': [
                                'web-main-content',
                            ],
                        },
                        'tagsSearchOptions': {
                            'numericFilters': 'postCount>=1',
                            'clickAnalytics': True,
                            'analyticsTags': [
                                'web-main-content',
                            ],
                        },
                        'listsSearchOptions': {
                            'clickAnalytics': True,
                            'analyticsTags': [
                                'web-main-content',
                            ],
                        },
                        'searchInCollection': False,
                        'collectionDomainOrSlug': 'medium.com',
                    },
                    'query': graph_query,
                },
            ]

            response = requests.post(url=url, headers=self.headers, json=json_data)
            if response.ok:
                json_data = response.json()
                results += get_attributes(json_data)
                pd.DataFrame(results).to_csv(results_file, index=False)

                count_valid_dics = sum(1 for d in results if validity_condition(d))
                if count_valid_dics >= 15:
                    break

        valid_dics = [d for d in results if validity_condition(d)]
        return valid_dics

    def get_post_content(self, post_url):
        try:
            response = requests.get(post_url, headers=self.headers)
            
            if response.ok:
                apollo_state = get_apollo_state(response.text)
                if apollo_state:
                    text = ''

                    for key, value in apollo_state.items():
                        if key.startswith("Paragraph"):
                            text += ' ' + value.get('text', '')

                return text
            
        except:
            pass
        
        return False