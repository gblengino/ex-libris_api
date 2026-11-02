from rest_framework.permissions import BasePermission, SAFE_METHODS

# Permiso de edicion sobre instancias del usuario
class IsAuthorOrReadOnly(BasePermission):

    """
    Al utilizar has_object_permission la comprobacion se realiza sobre un objeto creado,
    lo cual permite realizar peticiones 'GET' (a traves del method in SAFE_METHODS) sin
    ejercer control sobre las peticiones 'POST', lo cual me permite controlarla antes
    con otros permisos que trae rest_framework como, por ejemplo, IsAuthenticated y
    sus variantes.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.user == request.user