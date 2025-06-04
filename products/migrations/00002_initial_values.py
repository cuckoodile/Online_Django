from django.db import migrations

def create_initial_product_specification_names(apps, schema_editor):
    SpecificationName = apps.get_model('products', 'SpecificationName')

    # Add default product specification names
    SpecificationName.objects.get_or_create(id=3, defaults={'name': 'Gender'})
    SpecificationName.objects.get_or_create(id=4, defaults={'name': 'Material'})
    SpecificationName.objects.get_or_create(id=5, defaults={'name': 'Brand'})
    SpecificationName.objects.get_or_create(id=6, defaults={'name': 'Model'})

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_product_specification_names),
    ]