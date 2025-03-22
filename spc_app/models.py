from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=1000.0)  # Starting virtual funds

    def __str__(self):
        return f"{self.user.username}'s Account"

class DefensePrompt(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='defenses')
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Defense for {self.account.user.username} at {self.created_at}"

class AttackPrompt(models.Model):
    attacker = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='attacks')
    target_defense = models.ForeignKey(DefensePrompt, on_delete=models.CASCADE, related_name='attacks')
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    evaluation_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attack by {self.attacker.user.username} on {self.target_defense.account.user.username}"

class PromptLog(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    context = models.CharField(max_length=50)  # e.g., "defense", "attack", "evaluation"

    def __str__(self):
        return f"Log [{self.context}] at {self.timestamp}"
