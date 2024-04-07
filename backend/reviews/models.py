from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey


class AbstractReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Select the user who created this review')
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                               help_text='Enter the rating for this review (1 to 5)')
    title = models.CharField(max_length=256, help_text='Enter a title for this review')
    comment = models.TextField(help_text='Enter your comment or review here')
    objects = models.Manager()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     help_text='Content type of the related object')
    object_id = models.PositiveIntegerField(help_text='ID of the related object')
    content_object = GenericForeignKey()

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(user={self.user!r}, pk={self.pk!r}, title={self.title!r})"

    def __str__(self) -> str:
        return f"{self.title!s}"
