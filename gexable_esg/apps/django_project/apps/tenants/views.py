from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tenant


class CurrentTenantView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant_id = request.headers.get("X-Tenant-ID")
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
