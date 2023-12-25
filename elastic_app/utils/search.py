# elastic_app/utils/search.py

import json
import logging
from elasticsearch import Elasticsearch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Elasticsearch connection settings
es_url = "https://localhost:9200"
es = Elasticsearch(
    es_url,
    verify_certs=True,
    ca_certs="/Users/aakash.mahawar/http_ca.crt",
    basic_auth=('elastic', 'p+y11vnmA_RR-D3blhax')
)

# Index name
index_name = "movies"

def perform_search(query):
    """Perform the Elasticsearch search and return the results."""
    try:
        search_result = es.search(index=index_name, body=query)
        return search_result['hits']['hits']
    except Exception as e:
        logger.error(f"Error performing search: {e}")
        return []

def format_search_results(results):
    """Format the search results as a list of dictionaries."""
    formatted_results = []
    for hit in results:
        item = {
            'title': hit['_source'].get('title', ''),
            'director': hit['_source'].get('director', ''),
            'image': hit['_source'].get('image', ''),
            'url': hit['_source'].get('url', '')
        }
        formatted_results.append(item)
    return formatted_results

def search_movies(cast):
    """Search movies based on the provided cast."""
    search_query = {
        "query": {
            "match": {
                "cast": cast
            }
        }
    }

    # Perform the search
    search_results = perform_search(search_query)

    # Format the search results
    formatted_results = format_search_results(search_results)

    return formatted_results


