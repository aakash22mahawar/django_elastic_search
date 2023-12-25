from django.core.management.base import BaseCommand
from elastic_app.utils.scraper import scrape_data
import time

class Command(BaseCommand):
    help = 'Scrape data and index it in Elasticsearch'

    def handle(self, *args, **kwargs):
        start = time.time()
        scrape_data()
        end = time.time()
        print(f'**** time elapsed {round(end-start,2)} seconds ****')
