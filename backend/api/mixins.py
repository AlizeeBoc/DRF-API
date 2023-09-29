from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin:
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

#Filtre les objets selon l'utilisateur connecté
class UserQuerySetMixin():
     user_field = 'user' #variable "de filtrage"
     allow_staff_view = False # /
     def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs) # récupère tous les produits (Product.objects.all())
        if self.allow_staff_view and user.is_staff: # /
            return qs # /
        return qs.filter(**lookup_data) # récupère les products associés à cet user