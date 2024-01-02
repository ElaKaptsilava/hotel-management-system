from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey


class AbstractReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=256)
    comment = models.TextField()
    objects = models.Manager()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(user={self.user!r}, pk={self.pk!r}, title={self.title!r})"

    def __str__(self):
        return f"{self.title!s}"
