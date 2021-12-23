from django.db import models
from users.models import Developer


class Project(models.Model):
    owner = models.ForeignKey(
        Developer, on_delete=models.CASCADE, null=True, blank=False)
    title = models.CharField(max_length=30, blank=False, null=True)
    photo = models.ImageField(null=True, upload_to='proj_pic/',
                              default='proj_pic/proj-default.png', blank=True)
    description = models.CharField(max_length=400, blank=False, null=True)
    source_link = models.URLField(null=True, blank=True)
    like_count = models.IntegerField(default=0, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['id']


class Review(models.Model):
    owner = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=200, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.content

    
    class Meta:
        ordering = ['id']