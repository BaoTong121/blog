from django.db import models
from user.models import User
class Post(models.Model):
    class Meta:
        db_table = "post"
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    postdate = models.DateTimeField(null=False)
    author = models.ForeignKey(User)

    def __repr__(self):
        return "<{} {} {} {}>".format(self.id, self.title, self.author_id, self.content)

    __str__ = __repr__

class Content(models.Model):
    class Meta:
        db_table = "content"
    post = models.OneToOneField(Post)
    content = models.TextField(null=False)

    def __repr__(self):
        return "<{}>".format(self.content)

    __str__ = __repr__

# Create your models here.

