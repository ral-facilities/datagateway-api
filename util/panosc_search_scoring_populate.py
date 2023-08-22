import datetime

import requests
import os
import json
import time


def load_configuration(skip=0, limit=50):
    search_api_url = os.environ.get('SEARCH_API_URL', 'https://localhost:5000/search-api')  # Address of the search API
    score_api_url = os.environ.get('SCORE_API_URL', 'http://localhost:8000')  # Address of the scoring API

    document_filter = {
        'filter': json.dumps({
            'where': {
                   'summary': {
                       'ilike': None,
                   }
            },
            'include': [
                    {
                        'relation': 'members',
                        'scope': {
                            'include': [{'relation': 'person'}, {'relation': 'affiliation'}]
                        }
                    },
                    {
                        'relation': 'parameters',
                    },
                ],
            'skip': skip,
            'limit': limit
        })
    }

    document_mapper = {
        'title': lambda d: d.get('title', ''),
        'summary': lambda d: d.get('summary', ''),
        'type': lambda d: d.get('type', ''),
        'parameters': lambda d: [copy_dict(t, skip_fields=['id', 'documentId']) for t in d.get('parameters', [])],
        'members': lambda d: [
            {
                'role': m.get('role', ''),
                'person': copy_dict(m.get('person', {}) if m.get('person', {}) else {}, skip_fields=['id']),
                'affiliation': copy_dict(m.get('affiliation', {}) if m.get('affiliation', {}) else {}, skip_fields=['id']),
            } for m in d.get('members', [])
        ]
    }

    return {
        'search_api_url': search_api_url,
        'score_api_url': score_api_url,
        'document_filter': document_filter,
        'mappers': {
            'documents': document_mapper,
        },
    }


def load_documents(config):
    response = requests.get(
        url=f'{config["search_api_url"]}/documents',
        headers={'Accept': 'application/json'},
        params=config['document_filter']
    )
    return response.json()


# Create score data for datasets and documents
def copy_dict(d, skip_fields=None):
    skip = skip_fields if skip_fields is not None else []
    return {k: v for k, v in d.items() if k not in skip}


def extract(data, d_map, group):
    fields = {key: mapper(data) for key, mapper in d_map.items()}
    return {
        'id': data['pid'],
        'group': group,
        'fields': fields,
    }


# Clear score database
def clear_scoring_service(config):
    count = requests.get(f'{config["score_api_url"]}/items/count').json()['count']
    if count > 0:
        response = requests.get(
            url=f'{config["score_api_url"]}/items',
            params={
                'limit': count
            }
        )
        current_items = response.json()
        deleted_items = []
        for item in current_items:
            response = requests.delete(url='/'.join([f'{config["score_api_url"]}/items', item['id']]))
        deleted_items.append(response.status_code)


def upload_data(config, data):
    requests.post(
        url=f'{config["score_api_url"]}/items',
        json=data
    )


def compute_weight(config):
    requests.post(
        url=f'{config["score_api_url"]}/compute'
    )
    # Wait till compute finishes
    while requests.get(url=f'{config["score_api_url"]}/compute').json()['inProgress']:
        time.sleep(1)


if __name__ == "__main__":
    print(f"Script started at {datetime.datetime.now().time()}")

    skip = 0

    #while skip < 100:
    while True:
        print(f"Skip: {skip} | {datetime.datetime.now().time()}")
        configuration = load_configuration(skip=skip)
        documents = load_documents(config=configuration)
        if len(documents) == 0:
            print("Number of documents: 0 | Will stop script")
            break
        print(f"Number of documents: {len(documents)}")

        prepared_documents = [extract(document, configuration['mappers']['documents'], 'Documents') for
                              document in documents]
        # clear_scoring_service(config=configuration)
        upload_data(config=configuration, data=prepared_documents)
        print("Data uploaded to scoring service")
        # compute_weight(config=configuration)

        skip = skip + 50

    print(f"Script ended at {datetime.datetime.now().time()}")
