from django.db import models
from .BaseModel import BaseModel
from .Author import Author


class Book(BaseModel):
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default="Moby Dick")
    year = models.CharField(max_length=128, default="David Copperfield")
