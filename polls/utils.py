import httpx
import json
from basecamp_poll.settings import user_agent

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from users.models import CustomUser

def get_bc_user(user_email):
    user = CustomUser.objects.filter(email=user_email)[0]
    social_account = SocialAccount.objects.filter(user=user).first()

    return social_account

def get_app(app_name):
    basecamp = SocialApp.objects.filter(name=app_name).first()

    return basecamp

def get_bc_user_id(user_email):
    social_account = get_bc_user(user_email)
    user_id = social_account.extra_data['accounts'][0]['id']

    return user_id

def get_bc_user_token(user_email):
    basecamp = get_app("Basecamp")
    social_account = get_bc_user(user_email)
    token = SocialToken.objects.filter(account=social_account, app=basecamp).first().token

    return token

def get_all_bc_projects(user_email):
    basecamp = get_app("Basecamp")
    user_id = get_bc_user_id(user_email)
    social_account = get_bc_user(user_email)
    token = SocialToken.objects.filter(account=social_account, app=basecamp).first().token

    url = f"https://3.basecampapi.com/{user_id}/projects.json"
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': user_agent,
    }
        
    r = httpx.get(url, headers=headers)

    projects = json.loads(r.text)

    projects_list = []
    for project in projects:
        projects_list.append(project['name'])

    return projects_list
