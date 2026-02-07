from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.middleware.csrf import get_token
from .utils import process_image_to_fourier, process_vectors_to_fourier
import os
import json

def index(request):
    get_token(request)  # Ensure CSRF token is set
    return render(request, 'index.html')

def process_upload(request):
    num_coeffs = 500
    
    # Handle File Upload (Image)
    if request.method == 'POST' and request.FILES.get('drawing'):
        uploaded_file = request.FILES['drawing']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        try:
            # Returns LIST of coefficient sets
            coeffs_list = process_image_to_fourier(file_path, num_coefficients=num_coeffs)
            
            # Cleanup
            fs.delete(filename)
            
            return JsonResponse({'status': 'success', 'data': coeffs_list})
        except Exception as e:
             return JsonResponse({'status': 'error', 'message': str(e)})

    # Handle JSON Vector Data (Points from Frontend)
    elif request.method == 'POST' and request.body:
        try:
            data = json.loads(request.body)
            if 'strokes' in data:
                # Returns LIST of coefficient sets
                coeffs_list = process_vectors_to_fourier(data['strokes'], num_coefficients=num_coeffs)
                return JsonResponse({'status': 'success', 'data': coeffs_list})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'No valid data uploaded'})