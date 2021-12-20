
from django.db import models
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)




class Post(models.Model):
    TOPIC1 = 'Football'
    TOPIC2 = "Men's Basketball"
    TOPIC3 = "Women's basketball"
    TOPIC4 = "Softball"
    TOPIC5 = "Baseball"
    TOPIC6 = "Campus"
    TOPICS_CHOICES = (
        ('Football',TOPIC1),
        ("Men's Basketball",TOPIC2),
        ("Women's basketball",TOPIC3),
        ("Softball",TOPIC4),
        ("Baseball",TOPIC5),
        ("Campus",TOPIC6)
    )
    content = models.TextField(max_length=256, null=False)
    postImage = models.ImageField(_("Image"), upload_to=upload_to,null=True,blank=True)
    postLink = models.URLField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    postTime = models.DateTimeField(null=False)  # False
    isPublished = models.BooleanField(default=False)
    topic = models.CharField(
        max_length=50, choices=TOPICS_CHOICES, default=TOPICS_CHOICES[0][0],null=False)
    postLink = models.URLField(max_length=255,blank=True)

    class Meta:
        ordering = ['-postTime']

    def __str__(self):
        return str(self.id)
