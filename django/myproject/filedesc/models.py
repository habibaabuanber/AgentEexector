from djongo import models

class FileDescription(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.file_name
