from django.urls import path, include
from .views import (
    CandidateListApiView,
    CandidateDetailApiView,
    FileDownloadListAPIView
)

# api urls
urlpatterns = [
    path('', CandidateListApiView.as_view()),
    path('<int:candidate_id>/', CandidateDetailApiView.as_view()),
    path('download/<int:candidate_id>/', FileDownloadListAPIView.as_view())
]
