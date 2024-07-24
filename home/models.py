from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)

class Fingerprint(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    fingerprint_features = models.BinaryField()
    fingerprint_number = models.PositiveIntegerField()  # 1 to 6
