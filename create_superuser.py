"""
Script to create a Django superuser non-interactively
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'complaints_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Default superuser credentials
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

# Check if superuser already exists
if User.objects.filter(username=username).exists():
    print(f'Superuser "{username}" already exists!')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f'Password updated for existing superuser "{username}"')
else:
    # Create new superuser
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'Superuser "{username}" created successfully!')

print(f'\nLogin credentials:')
print(f'Username: {username}')
print(f'Password: {password}')
print(f'\nYou can now login at: http://127.0.0.1:8000/admin/')
