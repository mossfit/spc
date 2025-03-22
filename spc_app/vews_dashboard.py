from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from .models import DefensePrompt, AttackPrompt, Account

def dashboard_metrics(request):
    # Aggregate counts for defense and attack prompts
    total_defense = DefensePrompt.objects.count()
    total_attack = AttackPrompt.objects.count()
    flagged_count = AttackPrompt.objects.filter(successful=False).count()  # Assuming unsuccessful might be flagged
    success_rate = (
        AttackPrompt.objects.filter(successful=True).count() / total_attack * 100
        if total_attack > 0 else 0
    )
    
    # Average account balance (for balance trend metrics)
    avg_balance = Account.objects.all().aggregate(Avg('balance'))['balance__avg']
    
    metrics = {
        "total_defense_prompts": total_defense,
        "total_attack_prompts": total_attack,
        "flagged_prompts": flagged_count,
        "attack_success_rate": success_rate,
        "average_account_balance": avg_balance,
    }
    
    return JsonResponse(metrics)

def dashboard_leaderboard(request):
    accounts = Account.objects.all().order_by("-balance")
    leaderboard = [{
        "username": account.user.username,
        "balance": account.balance
    } for account in accounts]
    return JsonResponse({"leaderboard": leaderboard})
