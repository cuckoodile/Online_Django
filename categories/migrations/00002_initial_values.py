from django.db import migrations

def create_initial_categories_name(apps, schema_editor):
    CategoryName = apps.get_model('categories', 'Category')

    # Add default transaction types
    CategoryName.objects.get_or_create(id=1, defaults={'name': 'Jacket'})
    CategoryName.objects.get_or_create(id=2, defaults={'name': 'Pants'})
    CategoryName.objects.get_or_create(id=3, defaults={'name': 'Shoes'})
    CategoryName.objects.get_or_create(id=4, defaults={'name': 'Shirt'})
    CategoryName.objects.get_or_create(id=5, defaults={'name': 'T-Shirt'})
    CategoryName.objects.get_or_create(id=6, defaults={'name': 'Hoodie'})

class Migration(migrations.Migration):
    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories_name),
    ]