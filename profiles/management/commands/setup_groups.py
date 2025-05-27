from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

ROLE_GROUPS = {
    'Authorized Customer': [
        'products.view_product',
        'product_review.can_view_product_review',
        'product_review.can_add_product_review',
        'categories.view_category',
        'transactions.add_transaction',
        'transactions.change_transaction',
        'profiles.add_user',
        'profiles.change_user',
        'profiles.view_user',
        'profiles.add_profile',
        'profiles.change_profile',
        'profiles.view_profile',
    ],
    'Shipper/Logistic Partner': [
        'products.view_product',
        'transactions.view_transaction',
        'categories.view_category',
        'transactions.change_transaction',
        'profiles.change_user',
        'profiles.change_profile',
    ],
    'Orders Tracker': [
        'products.view_product',
        'transactions.view_transaction',
        'categories.view_category',
        'transactions.change_transaction',
        'profiles.change_user',
        'profiles.change_profile',
    ],
    'Admin': [
        'products.view_product',
        'products.add_product',
        'products.change_product',
        'products.delete_product',
        'categories.add_category',
        'categories.change_category',
        'categories.delete_category',
        'categories.view_category',
        'product_review.can_view_product_review',
        'product_review.can_add_product_review',
        'product_review.can_edit_product_review', 
        'product_review.can_delete_product_review',
        'transactions.view_transaction',
        'transactions.add_transaction',
        'transactions.change_transaction',
        'transactions.delete_transaction',
        'profiles.add_user',
        'profiles.change_user',
        'profiles.view_user',
        'profiles.delete_user',
        'profiles.add_profile',
        'profiles.change_profile',
        'profiles.view_profile',
        'profiles.delete_profile',
    ],
}

class Command(BaseCommand):
    help = 'Create default groups and assign permissions for roles.'

    def handle(self, *args, **options):
        for group_name, perms in ROLE_GROUPS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                app_label, codename = perm_codename.split('.')
                try:
                    perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permission {perm_codename} not found.'))
            group.save()
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" updated.'))
        self.stdout.write(self.style.SUCCESS('All groups and permissions set up.'))
