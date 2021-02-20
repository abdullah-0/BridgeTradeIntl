from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Relations(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='child')

    def __str__(self):
        return self.parent.name + ' Parent ' + self.child.name
