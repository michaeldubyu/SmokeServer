from django.db import models
from gcm.models import AbstractDevice

class MyDevice(AbstractDevice):
    pass

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, blank=False)
    friends_list = models.CommaSeparatedIntegerField(max_length=512)
    gcm_id = models.IntegerField(unique=True)

    def massage(self):
        self.friends_list = ",".join(set(self.friends_list))
        self.friends_list = self.friends_list.strip(",")

    def get_email_friends_list(self):
        friends_ids = self.friends_list.split(",")
        friends_email_list = []
        for uid in friends_ids:
            try :
                temp = User.objects.get(id=int(uid))
                friends_email_list.append(temp.email)
            except User.DoesNotExist:
                pass
        return friends_email_list

