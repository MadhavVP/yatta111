from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.middleware.csrf import get_token
from .utils import process_image_to_fourier
import os

def index(request):
    get_token(request)  # Ensure CSRF token is set
    return render(request, 'index.html')

def process_upload(request):
    if request.method == 'POST' and request.FILES.get('drawing'):
        uploaded_file = request.FILES['drawing']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        try:
            # Run the math!
            coeffs = process_image_to_fourier(file_path, num_coefficients=150)
            
            # Cleanup: Delete the file after processing to save space
            fs.delete(filename)
            
            return JsonResponse({'status': 'success', 'data': coeffs})
        except Exception as e:
             return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'No file uploaded'})