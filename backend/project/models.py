from django.db import models


class Project(models.Model):
    run_id = models.IntegerField()
    project_name = models.CharField(max_length=200)
    sample_id = models.IntegerField()
    sample_number = models.IntegerField(default=0)  # reserved
    sample_name = models.CharField(max_length=200)
    cell_number = models.IntegerField(default=0)
    read_number = models.IntegerField(default=0)
    smart_id = models.IntegerField()
    alfa_subsample_id = models.IntegerField()
    alfa_subsample_name = models.CharField(max_length=200, default='')  # reserved
    alfa_index_id = models.IntegerField()
    alfa_index_number = models.IntegerField(default=0)  # reserved
    beta_subsample_id = models.IntegerField()
    beta_subsample_name = models.CharField(max_length=200, default='')  # reserved
    beta_index_id = models.IntegerField()
    beta_index_number = models.IntegerField(default=0)  # reserved
    comments = models.TextField(blank=True)
