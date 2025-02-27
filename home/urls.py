from django.urls import path
from . import views
from django.conf.urls import handler404
from .views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    # Endpoints for loading classes, subjects, and chapters
    path('get-classes/', views.get_classes, name='get_classes'),
    path('get-subjects/<int:class_id>/', views.get_subjects, name='get_subjects'),
    path('get-chapters/<int:subject_id>/', views.get_chapters, name='get_chapters'),
    
    # Endpoint for general chapter resources (e.g., notes, books, etc.)
    path('get-resources/<int:chapter_id>/', views.get_resources, name='get_resources'),
    
    # Endpoints for specific resource types that require selection (quiz, questions, worksheet)
    path('get-quiz/<int:chapter_id>/', views.get_quiz, name='get_quiz'),
    path('get-questions/<int:chapter_id>/', views.get_questions, name='get_questions'),
    path('get-worksheets/<int:chapter_id>/', views.get_worksheets, name='get_worksheets'),
    path("get-ch/<str:classname>/<str:subject_name>/", views.get_chapters_name, name="getchname"),

    # Optionally add any other endpoints (e.g., index, contacts, etc.)
    path('', views.index, name='index'),
    path('contacts/', views.Contacts, name='contacts'),
    path('download/', views.download, name='download'),
    path('quiz/<str:classname>/<str:subjectname>/<str:chapter_name>/<str:title>', views.Quizs, name='quiz'),
    
    path('questions/<str:classname>/<str:subjectname>/<str:chapter_name>/<str:title>', views.questionss, name='question'),
    
    path('worksheet/<str:classname>/<str:subjectname>/<str:chapter_name>/<str:title>', views.work, name='quiz'),
path('<str:classname>/<str:subjectname>/<str:chapter_name>/<str:rec>', views.book, name='book'),
 path("class/<str:class_name>/", views.classes, name="classes"),

    
]
