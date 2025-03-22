from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Account, DefensePrompt, AttackPrompt, PromptLog
from .services.llm_api import evaluate_prompt
from .services.malware_detection import is_prompt_suspicious
from django.contrib.auth.models import User

@csrf_exempt
def submit_defense(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        prompt_text = data.get("prompt_text")
        
        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(user=user)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Account.DoesNotExist:
            return JsonResponse({"error": "Account not found."}, status=404)
        
        defense = DefensePrompt.objects.create(account=account, prompt_text=prompt_text)
        return JsonResponse({"message": "Defense prompt submitted successfully.", "defense_id": defense.id})
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def submit_attack(request):
    if request.method == "POST":
        data = json.loads(request.body)
        attacker_username = data.get("attacker_username")
        defense_id = data.get("defense_id")
        prompt_text = data.get("prompt_text")
        
        try:
            attacker = User.objects.get(username=attacker_username)
            attacker_account = Account.objects.get(user=attacker)
            defense = DefensePrompt.objects.get(id=defense_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Attacker user not found."}, status=404)
        except Account.DoesNotExist:
            return JsonResponse({"error": "Attacker account not found."}, status=404)
        except DefensePrompt.DoesNotExist:
            return JsonResponse({"error": "Defense prompt not found."}, status=404)
        
        # Evaluate the attack prompt against the defense prompt using our LLM API integration.
        eval_result = evaluate_prompt(defense.prompt_text, prompt_text)

        flagged = is_prompt_suspicious(prompt_text)

        attack = AttackPrompt.objects.create(
            attacker=attacker_account,
            target_defense=defense,
            prompt_text=prompt_text,
            successful=eval_result["successful"],
            evaluation_response=eval_result["response"]
        )

        # Log the evaluation along with the flag status.
        PromptLog.objects.create(
            prompt=f"Defense: {defense.prompt_text} | Attack: {prompt_text}",
            response=eval_result["response"],
            context="evaluation",
            flagged=flagged
        )
        
        attack = AttackPrompt.objects.create(
            attacker=attacker_account,
            target_defense=defense,
            prompt_text=prompt_text,
            successful=eval_result["successful"],
            evaluation_response=eval_result["response"]
        )
        
        # Optionally, update balances (simplified logic)
        if eval_result["successful"]:
            # Transfer funds: e.g., attacker gains 10 points; defender loses 10 points
            attacker_account.balance += 10
            defense.account.balance -= 10
            attacker_account.save()
            defense.account.save()
        
        # Log the prompt interaction
        PromptLog.objects.create(
            prompt=f"Defense: {defense.prompt_text} | Attack: {prompt_text}",
            response=eval_result["response"],
            context="evaluation"
        )
        
        return JsonResponse({
            "message": "Attack prompt submitted and evaluated.",
            "attack_id": attack.id,
            "successful": eval_result["successful"],
            "response": eval_result["response"]
        })
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def get_leaderboard(request):
    if request.method == "GET":
        # Retrieve all accounts and sort by balance descending.
        accounts = Account.objects.all().order_by("-balance")
        leaderboard = []
        for account in accounts:
            leaderboard.append({
                "username": account.user.username,
                "balance": account.balance
            })
        return JsonResponse({"leaderboard": leaderboard})
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
