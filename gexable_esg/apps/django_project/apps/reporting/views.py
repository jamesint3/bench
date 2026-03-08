from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.request_context import get_tenant_id
from apps.users.authentication import AuthenticatedUserPermission, BearerTokenAuthentication

from .models import ReportRun
from .selectors import list_export_jobs, list_report_runs, list_templates
from .services import create_export_job, create_report_run, create_template, deliver_report


class ReportingBaseView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [AuthenticatedUserPermission]

    def tenant_id(self, request):
        return get_tenant_id(request)


class ReportTemplateListCreateView(ReportingBaseView):
    def get(self, request):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list(list_templates(tenant_id=tenant_id)))

    def post(self, request):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        payload = {
            "name": request.data.get("name"),
            "framework": request.data.get("framework"),
            "file_format": request.data.get("file_format", "pdf"),
            "template_config": request.data.get("template_config", {}),
        }
        if not payload["name"] or not payload["framework"]:
            return Response({"detail": "name and framework are required"}, status=status.HTTP_400_BAD_REQUEST)
        template = create_template(tenant_id=tenant_id, payload=payload, requested_by_id=request.user.id)
        return Response({"id": template.id, "name": template.name, "framework": template.framework}, status=status.HTTP_201_CREATED)


class ReportRunListCreateView(ReportingBaseView):
    def get(self, request):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list(list_report_runs(tenant_id=tenant_id)))

    def post(self, request):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        template_id = request.data.get("template_id")
        if not template_id:
            return Response({"detail": "template_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        run = create_report_run(tenant_id=tenant_id, payload={"template_id": template_id}, requested_by_id=request.user.id)
        return Response({"id": run.id, "status": run.status, "template_id": run.template_id}, status=status.HTTP_201_CREATED)


class ReportRunDeliveryView(ReportingBaseView):
    def post(self, request, run_id: int):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        run = ReportRun.objects.filter(id=run_id, tenant_id=tenant_id).first()
        if not run:
            return Response({"detail": "report run not found"}, status=status.HTTP_404_NOT_FOUND)
        emails = request.data.get("emails", [])
        if not emails:
            return Response({"detail": "emails are required"}, status=status.HTTP_400_BAD_REQUEST)
        result = deliver_report(tenant_id=tenant_id, report_run=run, emails=emails)
        return Response({"run_id": run.id, **result})


class ExportJobListCreateView(ReportingBaseView):
    def get(self, request):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(list(list_export_jobs(tenant_id=tenant_id)))

    def post(self, request):
        tenant_id = self.tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)
        report_run_id = request.data.get("report_run_id")
        if not report_run_id:
            return Response({"detail": "report_run_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        export = create_export_job(
            tenant_id=tenant_id,
            payload={"report_run_id": report_run_id, "export_type": request.data.get("export_type", "csv")},
        )
        return Response({"id": export.id, "status": export.status, "export_type": export.export_type}, status=status.HTTP_201_CREATED)
