from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, blank=False)
    friends_list = models.CharField(max_length=64)

    class Meta:
        ordering = ('id', )

