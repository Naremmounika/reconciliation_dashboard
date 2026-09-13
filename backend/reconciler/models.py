from django.db import models


class Location(models.Model):
    location_id = models.CharField(max_length=100, unique=True)
    org_id = models.CharField(max_length=100)
    location_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location_id} - {self.org_id}"


class SystemARecord(models.Model):
    record_id = models.CharField(max_length=100, unique=True)
    location_id = models.CharField(max_length=100, blank=True)
    event_date = models.CharField(max_length=100, blank=True)
    category_code = models.CharField(max_length=100, blank=True)
    actor_id = models.CharField(max_length=100, blank=True)

    base_value = models.TextField(blank=True)
    adjustment = models.TextField(blank=True)
    total_value = models.TextField(blank=True)
    state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.record_id


class SystemBEntry(models.Model):
    entry_id = models.CharField(max_length=100, unique=True)
    record_ref = models.CharField(max_length=100, blank=True)
    normalized_record_ref = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )
    location_id = models.CharField(max_length=100, blank=True)
    recorded_on = models.CharField(max_length=100, blank=True)
    value = models.TextField(blank=True)
    label = models.TextField(blank=True)

    def __str__(self):
        return self.entry_id