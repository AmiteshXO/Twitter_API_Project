from django.db import models

# Create your models here.

class Tweet_author(models.Model):
	person = models.TextField()
	def __str__(self):
		return self.person

class Tweet(models.Model):
	tweet_person = models.ForeignKey(Tweet_author,on_delete=models.CASCADE)
	tweet_id = models.CharField(max_length=250,null=True,blank=True)
	tweet_domain = models.CharField(max_length=250,null=True,blank=True)
	def __str__(self):
		return self.tweet_domain