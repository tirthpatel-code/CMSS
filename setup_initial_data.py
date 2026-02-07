"""
Script to create initial complaint categories
Run this after creating a superuser: python manage.py shell < setup_initial_data.py
Or run: python manage.py shell
Then copy-paste the code below
"""

from complaints.models import ComplaintCategory

categories = [
    ('Technical Issue', 'Hardware, software, or technical problems'),
    ('Service Complaint', 'Issues with service delivery or quality'),
    ('Billing Issue', 'Problems related to billing or payments'),
    ('Facility Issue', 'Problems with facilities or infrastructure'),
    ('Staff Behavior', 'Complaints about staff conduct or behavior'),
    ('Product Quality', 'Issues with product quality or defects'),
    ('Delivery Issue', 'Problems with delivery or shipping'),
    ('Other', 'Other types of complaints'),
]

for name, description in categories:
    category, created = ComplaintCategory.objects.get_or_create(
        name=name,
        defaults={'description': description}
    )
    if created:
        print(f'Created category: {name}')
    else:
        print(f'Category already exists: {name}')

print('\nInitial categories setup complete!')
