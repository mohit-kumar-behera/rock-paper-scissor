from django.db import models


class Room(models.Model):
	u_id = models.CharField(max_length=60,unique=True)
	def __str__(self):
		return self.u_id
	class Meta:
		verbose_name_plural = "Room"


class player(models.Model):
	join_id = models.ForeignKey(Room,on_delete=models.CASCADE)
	player_name = models.CharField(max_length=15)
	points_decided = models.IntegerField(default=10)
	creater = models.BooleanField(default=True)
	rps_choice = models.CharField(max_length=8,blank=True,null=True)
	def __str__(self):
		return self.player_name + " of Room " + self.join_id.u_id
	class Meta:
		verbose_name_plural = "Player"
