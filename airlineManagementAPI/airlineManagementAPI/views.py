from django.http import JsonResponse

def not_found(request, exception):
    response_data = {
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist. Please check the URL.",
        "status": 404
    }
    return JsonResponse(response_data, status=404)
