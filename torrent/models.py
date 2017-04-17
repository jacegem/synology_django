from django.db import models

# Create your models here.


class Magnet(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=100, db_index=True)
    title = models.TextField()
    magnet = models.CharField(max_length=100, db_index=True)
    reg_date = models.DateTimeField(db_index=True, auto_now_add=True)

    def get_absolute_url(self):
        return self.magnet
