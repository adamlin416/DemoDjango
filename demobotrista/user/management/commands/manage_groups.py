# user/management/commands/create_groups.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Create manager group and assign permissions
        manager_group, created = Group.objects.get_or_create(name="Manager")
        manager_permissions = [
            "add_product",
            "change_product",
            "delete_product",
            "view_product",
            "can_list_users",
            "can_manage_products",
        ]
        new_m_perms = []
        for codename in manager_permissions:
            perm = Permission.objects.get(codename=codename)
            if not manager_group.permissions.filter(codename=codename).exists():
                new_m_perms.append(perm)
        manager_group.permissions.add(*new_m_perms)

        # Create customer group and assign permissions
        customer_group, created = Group.objects.get_or_create(name="Customer")
        customer_permissions = [
            "view_order",
            "add_order",
            "change_order",
            "delete_order",
            "can_order",
        ]

        new_c_perms = []
        for codename in customer_permissions:
            perm = Permission.objects.get(codename=codename)
            if not customer_group.permissions.filter(codename=codename).exists():
                new_c_perms.append(perm)
        customer_group.permissions.add(*new_c_perms)

        if new_m_perms or new_c_perms:
            manager_group.save()
            customer_group.save()

            self.stdout.write(
                self.style.SUCCESS("User groups and permissions created successfully")
            )
