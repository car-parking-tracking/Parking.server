from django.db import models


class SingletonModel(models.Model):

    def delete(self, *args, **kwargs):  # pylint: disable=arguments-differ
        pass

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.pk is not None:
            super(SingletonModel, self).save(*args, **kwargs)
        else:
            self.pk = 1
            self.save()

    class Meta:
        abstract = True
