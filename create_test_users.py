import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User

def create_user(username, password, role, first_name, last_name):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        print(f"User {username} created with role {role}")
    else:
        print(f"User {username} already exists")

create_user('ai_user', 'password123', 'ai', 'AI', 'Agent')
create_user('inspektsiya_user', 'password123', 'inspektsiya', 'Inspektsiya', 'Xodim')
create_user('dekanat_user', 'password123', 'dekanat', 'Dekanat', 'Xodim')
create_user('rektor_user', 'password123', 'rektor', 'Rektor', 'Rahbar')

print("Test users creation script completed.")
