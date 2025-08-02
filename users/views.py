from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already taken'})
        
        user = User.objects.create_user(username=username, password=password1)
        return JsonResponse({'status': 'success', 'message': 'User registered successfully'})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
