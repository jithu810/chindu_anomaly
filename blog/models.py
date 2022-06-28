from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from pathlib import Path
from users.models import Space
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ValidationError

def find(instance, filename):
	num = Space.objects.get(name=instance.author)
	filesize = instance.file.size
	plan=(num.num)
	root_directory = Path('./media/'+str(instance.author))
	size=sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
	if filesize<int(plan):
		if size<int(plan):
			return '{0}/{1}'.format(instance.author, filename)
		else:
			raise ValidationError("Max limit reached")
	else:
		raise ValidationError("folder size is large")



class Post(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to=find)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

    
	
