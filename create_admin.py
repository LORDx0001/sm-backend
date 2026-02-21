import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Superuser 'admin' created with password 'admin'")
    else:
        user = User.objects.get(username='admin')
        user.set_password('admin')
        user.save()
        print("Superuser 'admin' password reset to 'admin'")
except Exception as e:
    print(f"Error: {e}")
