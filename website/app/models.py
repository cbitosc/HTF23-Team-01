from django.db import models

# Create your models here.
class SignUP(models.Model):
    uname = models.CharField(max_length=100)
    # password = models.CharField(max_length=50)
    image = models.ImageField(default='hacker.jpg',upload_to='images')
    passwords = models.CharField(max_length=100000000,default="eydmYWNlYm9vayc6Tm9uZSwnaW5zdGFncmFtJzpOb25lLCd0d2l0dGVyJzpOb25lLCdzcG90aWZ5JzpOb25lLCdkcm9wYm94JzpOb25lLCdnb29nbGUnOk5vbmV9")
    def __str__(self) -> str:
        return self.uname