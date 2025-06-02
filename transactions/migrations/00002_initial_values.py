from django.db import migrations

def create_initial_transaction_types_status_and_methods(apps, schema_editor):
    TransactionType = apps.get_model('transactions', 'TransactionType')
    TransactionMethod = apps.get_model('transactions', 'TransactionMethod')
    TransactionStatus = apps.get_model('transactions', 'TransactionStatus')

    # Add default transaction types
    TransactionType.objects.get_or_create(id=1, defaults={'name': 'Inbound'})
    TransactionType.objects.get_or_create(id=2, defaults={'name': 'Outbound'})

    # Add default transaction methods
    TransactionMethod.objects.get_or_create(id=1, defaults={'name': 'Cash on Delivery'})
    TransactionMethod.objects.get_or_create(id=2, defaults={'name': 'Paymaya'})
    TransactionMethod.objects.get_or_create(id=3, defaults={'name': 'GCash'})
    TransactionMethod.objects.get_or_create(id=4, defaults={'name': 'Bank'})

    # Add default transaction statuses
    TransactionStatus.objects.get_or_create(id=1, defaults={'name': 'Order Confirmation'})
    TransactionStatus.objects.get_or_create(id=2, defaults={'name': 'Shipping'})
    TransactionStatus.objects.get_or_create(id=3, defaults={'name': 'Received'})
    TransactionStatus.objects.get_or_create(id=4, defaults={'name': 'Done'})

class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_transaction_types_status_and_methods),
    ]