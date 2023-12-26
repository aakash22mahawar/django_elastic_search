from elasticsearch import Elasticsearch, ConnectionError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Elasticsearch connection settings
es_url = "https://localhost:9200"
ca_certificate_path = "/Users/aakash.mahawar/http_ca.crt"
es = Elasticsearch(
    es_url,
    verify_certs=True,
    ca_certs=ca_certificate_path,
    basic_auth=('username', 'password')
)

# Index settings and mappings
index_name = "movies"
mappings = {
    "properties": {
        "url": {"type": "text"},
        "title": {"type": "text", "analyzer": "english"},
        "image": {"type": "text"},
        "director": {"type": "text", "analyzer": "standard"},
        "cast": {"type": "keyword"},
        # Add other fields here
    }
}

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings =mappings)
    logger.info(f"Index '{index_name}' created successfully.")

def index_scraped_item(scraped_item):
    try:
        es.index(index="movies", body=scraped_item)
        logger.info("Item indexed successfully.")
    except ConnectionError as e:
        logger.error(f"Connection error while indexing: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while indexing: {e}")


