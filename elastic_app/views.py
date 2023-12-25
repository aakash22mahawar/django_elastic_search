# myapp/views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from elastic_app.utils.search import search_movies
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def search_view(request):
    if request.method == 'POST':
        cast = request.POST.get('query', '')
        cast = cast.title()

        logger.info(f"Received POST request with cast: {cast}")

        # Perform the search using the backend script
        search_results = search_movies(cast)
        context = {'results': search_results, 'cast': cast}

        # Render the form and results using a template
        return render(request, 'search_results.html', context=context)

    # Display the search form initially
    return render(request, 'search_results.html')
