"""
Script to create a regular user account
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'complaints_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create a regular user
username = 'user'
email = 'user@example.com'
password = 'user123'
first_name = 'John'
last_name = 'Doe'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f'User "{username}" already exists!')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.is_staff = False
    user.is_superuser = False
    user.save()
    print(f'Password and details updated for existing user "{username}"')
else:
    # Create new user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_staff=False,
        is_superuser=False
    )
    print(f'Regular user "{username}" created successfully!')

print(f'\nUser Login Credentials:')
print(f'Username: {username}')
print(f'Password: {password}')
print(f'Name: {first_name} {last_name}')
print(f'Email: {email}')
print(f'\nYou can now login at: http://127.0.0.1:8000/login/')
print(f'\nNote: This is a regular user account (not admin).')
print(f'Regular users can:')
print(f'  - Create complaints')
print(f'  - View their own complaints')
print(f'  - Add comments to their complaints')
print(f'  - View complaint history')
