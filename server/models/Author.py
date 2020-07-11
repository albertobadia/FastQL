from django.db import models
from .BaseModel import BaseModel


class Author(BaseModel):
    names = models.CharField(max_length=128, default="Charles")
    last_name = models.CharField(max_length=128, default="Dickends")
