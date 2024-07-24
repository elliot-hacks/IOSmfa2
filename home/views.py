from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Person, Fingerprint
from .forms import FingerprintForm
from .utils import extract_features
import numpy as np
import pickle

def register_fingerprints(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    fingerprints = Fingerprint.objects.filter(person=person)
    if len(fingerprints) >= 6:
        return redirect('attendance_success')
    
    if request.method == 'POST':
        form = FingerprintForm(request.POST, request.FILES)
        if form.is_valid():
            fingerprint_image = form.cleaned_data['fingerprint_image']
            features = extract_features(fingerprint_image.temporary_file_path())
            fingerprint = Fingerprint(
                person=person,
                fingerprint_features=pickle.dumps(features),
                fingerprint_number=len(fingerprints) + 1
            )
            fingerprint.save()
            return redirect('register_fingerprints', person_id=person.id)
    else:
        form = FingerprintForm()
    
    return render(request, 'attendance/register_fingerprints.html', {'form': form, 'person': person, 'fingerprints': fingerprints})

def authenticate(request):
    if request.method == 'POST':
        form = FingerprintForm(request.POST, request.FILES)
        if form.is_valid():
            fingerprint_image = form.cleaned_data['fingerprint_image']
            input_features = extract_features(fingerprint_image.temporary_file_path())
            persons = Person.objects.all()
            for person in persons:
                fingerprints = Fingerprint.objects.filter(person=person)
                for fingerprint in fingerprints:
                    stored_features = pickle.loads(fingerprint.fingerprint_features)
                    if np.allclose(input_features, stored_features, atol=0.05):  # Adjust tolerance as needed
                        # Mark arrival for person
                        # Add your arrival marking logic here
                        return JsonResponse({'status': 'success', 'person': person.id})
            return JsonResponse({'status': 'failure'})
    else:
        form = FingerprintForm()
    
    return render(request, 'attendance/authenticate.html', {'form': form})
