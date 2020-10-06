from django.db import models

from project.models import Project


RUN_STATUS = (('open', 'Open'), ('closed', 'Closed'), ('archived', 'Archived'))


class Run(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=RUN_STATUS, default='open')

    def num_of_projects(self):
        project_list = Project.objects.filter(run_id=self.id)
        return len(project_list)

