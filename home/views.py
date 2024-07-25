from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Person, Fingerprint
from .forms import FingerprintForm
from .tasks import extract_features_task, train_model_task
import pickle
import numpy as np

def register_fingerprints(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    fingerprints = Fingerprint.objects.filter(person=person)
    if len(fingerprints) >= 6:
        return redirect('attendance_success')
    
    if request.method == 'POST':
        form = FingerprintForm(request.POST, request.FILES)
        if form.is_valid():
            fingerprint_image = form.cleaned_data['fingerprint_image']
            features = extract_features_task(fingerprint_image.temporary_file_path()).get()
            fingerprint = Fingerprint(
                person=person,
                fingerprint_features=pickle.dumps(features),
                fingerprint_number=len(fingerprints) + 1
            )
            fingerprint.save()

            if len(fingerprints) + 1 == 6:
                train_model_task.delay()
            
            messages.success(request, 'Fingerprint uploaded successfully.')
            return redirect('register_fingerprints', person_id=person.id)
    else:
        form = FingerprintForm()
    
    return render(request, 'attendance/register_fingerprints.html', {'form': form, 'person': person, 'fingerprints': fingerprints})

def authenticate(request):
    if request.method == 'POST':
        form = FingerprintForm(request.POST, request.FILES)
        if form.is_valid():
            fingerprint_image = form.cleaned_data['fingerprint_image']
            input_features = extract_features_task(fingerprint_image.temporary_file_path()).get()

            with open('knn_model.pkl', 'rb') as f:
                knn = pickle.load(f)
            
            predicted_person_id = knn.predict([input_features])[0]

            try:
                person = Person.objects.get(id=predicted_person_id)
                messages.success(request, 'Authentication successful.')
                return JsonResponse({'status': 'success', 'person': person.id})
            except Person.DoesNotExist:
                messages.error(request, 'Authentication failed.')
                return JsonResponse({'status': 'failure'})
    else:
        form = FingerprintForm()
    
    return render(request, 'fingerprints/authenticate.html', {'form': form})


