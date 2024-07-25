from celery import shared_task
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
from .models import Fingerprint, Person
from .utils import extract_features

@shared_task
def extract_features_task(image_path):
    return extract_features(image_path)

@shared_task
def train_model_task():
    fingerprints = Fingerprint.objects.all()
    X = []
    y = []

    for fingerprint in fingerprints:
        features = pickle.loads(fingerprint.fingerprint_features)
        X.append(features)
        y.append(fingerprint.person.id)

    X = np.array(X)
    y = np.array(y)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    with open('knn_model.pkl', 'wb') as f:
        pickle.dump(knn, f)
