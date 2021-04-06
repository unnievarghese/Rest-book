from django.db import models

# Create your models here.
class book(models.Model):
    book_name=models.CharField(max_length=120,unique=True)
    book_price=models.IntegerField()
    book_pages=models.IntegerField()
    book_author=models.CharField(max_length=120)

    def __str__(self):
        return self.book_name