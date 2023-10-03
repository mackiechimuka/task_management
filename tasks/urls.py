from django.urls import path
from .views import AdminTaskView,TaskAllView,RetrieveTaskView,RetrieveAllTaskView

urlpatterns = [
    path('adminview/', AdminTaskView.as_view(), name='add_task_get_all_tasks'),
    path('adminview/<int:pk>/', RetrieveTaskView.as_view(), name='get_task_delete_task'),
    path('my-tasks/', TaskAllView.as_view(), name='my_tasks'),
    path('my-tasks/<int:pk>/', RetrieveAllTaskView.as_view(), name='update_task_view_tasks'),
]
