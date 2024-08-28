from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-timestamp']  
    
    def __str__(self):
        return " Sender--> " + str(self.sender) + "  , " + " Receiver--> " + str(self.receiver) 

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-created_at'] 
    
    def __str__(self):
        return " Sender--> " + str(self.user1) + "  , " + " Receiver--> " + str(self.user2) 

