from django.http import JsonResponse
from aviation.tasks import send_welcome_email

def test_email(request):
    result = send_welcome_email.delay("test@example.com")
    return JsonResponse({
        "task_id": result.id,
        "status": "queued"
    })