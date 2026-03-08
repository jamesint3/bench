from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.request_context import get_tenant_id

from .models import Tenant


class CurrentTenantView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        tenant_id = get_tenant_id(request)
        tenant = Tenant.objects.filter(id=tenant_id).first() if tenant_id else Tenant.objects.first()
        if not tenant:
            return Response({"tenant": None})
        return Response(
            {
                "tenant": {
                    "id": tenant.id,
                    "name": tenant.name,
                    "slug": tenant.slug,
                    "timezone": tenant.timezone,
                    "status": tenant.status,
                }
            }
        )
