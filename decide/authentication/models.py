from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class DecideUser(models.Model):
    SEX_CHOICES = (
        ('0', 'Female',),
        ('1', 'Male',),
        ('2', 'Unsure',),
    )    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
    )


    class Meta:
        ordering = ('-birthday',)

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.user.first_name, self.user.last_name, self.birthday, self.sex)
