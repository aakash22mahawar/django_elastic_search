# myapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from elastic_app.utils.search import search_movies
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def search_view(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            if request.method == 'POST':
                data = request.POST
            else:
                data = request.GET

            search_query = data.get('query', '')

            logger.info(f"Received {request.method} request with query: {search_query}")

            # Perform the search using the backend script
            search_results = search_movies(search_query)

            # Return the search results
            return JsonResponse({'results': search_results}, json_dumps_params={'indent': 4})

        except Exception as e:
            logger.error(f"Error processing search request: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
