from django.urls import path
from .Controllers.User import messageController

app_name = 'messages'

from django.urls import path

urlpatterns = [
    path('admin/reports/', messageController.admin_reports_view, name='admin_reports_view'),
    path('admin/reports/view_report/<int:report_id>/', messageController.view_report, name='view_report'),
    path('admin/reports/mark_handled/<int:report_id>/', messageController.mark_report_handled, name='mark_report_handled'),
    path('admin/reports/ban_user/<int:user_id>/', messageController.ban_user, name='ban_user'),
    path('send_message/<int:reported_profile_id>', messageController.send_report_message, name='send_message'),
]
