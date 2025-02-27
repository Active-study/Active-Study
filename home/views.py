from django.shortcuts import render ,HttpResponse
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse, Http404
from django.http import JsonResponse
from .models import Class, Subject, Chapter, ChapterResource ,Quiz, Questionsheet, Worksheet

def get_classes(request):
    classes = Class.objects.all().values('id', 'class_name')
    return JsonResponse(list(classes), safe=False)

def get_subjects(request, class_id):
    subjects = Subject.objects.filter(class_fk_id=class_id).values('id', 'subject_name')
    return JsonResponse(list(subjects), safe=False)

def get_chapters(request, subject_id):
    chapters = Chapter.objects.filter(subject_fk_id=subject_id).values('id', 'chapter_name')
    return JsonResponse(list(chapters), safe=False)

def get_chapters_name(request, classname, subject_name):
    try:
        subject = Subject.objects.get(class_fk__class_name=classname, subject_name=subject_name)
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)
    
    chapters = Chapter.objects.filter(subject_fk=subject).values('id', 'chapter_name')
    return JsonResponse(list(chapters), safe=False)

def get_resources(request, chapter_id):
    resources = ChapterResource.objects.filter(chapter_id=chapter_id).first()
    data = {
        'notes': None,
        'english_book': None,
        'hindi_book': None,
        'ncert_sol': None,
        'mind_map': None
    }
    if resources:
        data['notes'] = resources.notes_file.url if resources.notes_file else None
        data['english_book'] = resources.english_book_file.url if resources.english_book_file else None
        data['hindi_book'] = resources.hindi_book_file.url if resources.hindi_book_file else None
        data['ncert_sol'] = resources.ncert_sol_file.url if resources.ncert_sol_file else None
        data['mind_map'] = resources.mind_map.url if resources.mind_map else None
    return JsonResponse(data)





def get_quiz(request, chapter_id):
   
    quizzes = Quiz.objects.filter(chapter_id=chapter_id)
    data = [
        {
            'id': quiz.id,
            'title': quiz.title if quiz.title else f'Quiz {quiz.id}',
            'url': quiz.quiz_file.url if quiz.quiz_file else ''
        }
        for quiz in quizzes
    ]
    return JsonResponse(data, safe=False)







def get_questions(request, chapter_id):
    questions = Questionsheet.objects.filter(chapter_id=chapter_id)
    data = [
        {
            'id': qs.id,
            'title': qs.title if qs.title else f'Questionsheet {qs.id}',
            'url': qs.question_sheet_file.url if qs.question_sheet_file else ''
        }
        for qs in questions
    ]
    return JsonResponse(data, safe=False)

def get_worksheets(request, chapter_id):
    worksheets = Worksheet.objects.filter(chapter_id=chapter_id)
    data = [
        {
            'id': ws.id,
            'title': ws.title if ws.title else f'Worksheet {ws.id}',
            'url': ws.worksheet_file.url if ws.worksheet_file else ''
        }
        for ws in worksheets
    ]
    return JsonResponse(data, safe=False)

def index(request):
    return render(request,'index.html')
def Contacts(request):
    return render(request,"Contacts.html")
def download(request):
    return render(request ,"app_download.html")

def Quizs(request, classname, subjectname, chapter_name, title):
    # Retrieve the quiz that matches the given chapter name and quiz title.
    # We assume that the Chapter model has a field `chapter_name` and that the Quiz is linked to it.
    print("this")
    quiz = get_object_or_404(Quiz, chapter__chapter_name=chapter_name, title=title)

    # Get the URL of the quiz file (if one is uploaded)
    quiz_url = quiz.quiz_file.url if quiz.quiz_file else ""

    # Prepare the context data for the template. You might want to pass additional
    # information such as the class name, subject name, etc.
    context = {
        "quiz_url": quiz_url,
        "quiz": quiz,
        "classname": classname,
        "subjectname": subjectname,
        "chapter_name": chapter_name,
        "title": title,
    }
    
    # Render the 'quiz.html' template with the context data.
    return render(request, "quiz.html", context)
def questionss(request, classname, subjectname, chapter_name, title):
    # Retrieve the quiz that matches the given chapter name and quiz title.
    # We assume that the Chapter model has a field `chapter_name` and that the Quiz is linked to it.
    print("this")
    que = get_object_or_404(Questionsheet, chapter__chapter_name=chapter_name, title=title)

    # Get the URL of the quiz file (if one is uploaded)
    que_url = que.question_sheet_file.url if que.question_sheet_file else ""

    # Prepare the context data for the template. You might want to pass additional
    # information such as the class name, subject name, etc.
    context = {
        "que_url": que_url,
        
        "classname": classname,
        "subjectname": subjectname,
        "chapter_name": chapter_name,
        "title": title,
    }
    print(context)
    # Render the 'quiz.html' template with the context data.
    return render(request, "question.html", context)
def work(request, classname, subjectname, chapter_name, title):
    # Retrieve the quiz that matches the given chapter name and quiz title.
    # We assume that the Chapter model has a field `chapter_name` and that the Quiz is linked to it.
    print("this")
    work = get_object_or_404(Worksheet, chapter__chapter_name=chapter_name, title=title)

    # Get the URL of the quiz file (if one is uploaded)
    work_url = work.worksheet_file.url if work.worksheet_file else ""

    # Prepare the context data for the template. You might want to pass additional
    # information such as the class name, subject name, etc.
    context = {
        "work_url": work_url,
         "classname": classname,
        "subjectname": subjectname,
        "chapter_name": chapter_name,
        "title": title,
    }
    return render(request, "worksheet.html", context)
    



import json


def get_quiz_titles_as_json(class_name: str, subject_name: str, chapter_name: str):
    """Fetch all quiz titles for a given chapter and return them as JSON."""
    try:
        # Fetch the Chapter instance using class, subject, and chapter names
        chapter = Chapter.objects.get(
            subject_fk__class_fk__class_name__iexact=class_name.replace("_", " "),
            subject_fk__subject_name__iexact=subject_name.replace("_", " "),
            chapter_name__iexact=chapter_name.replace("_", " ")
        )

        # Fetch all quiz titles for the chapter
        quiz_titles = chapter.quizzes.values_list('title', flat=True)
        result = {
            "class_name": class_name,
            "subject_name": subject_name,
            "chapter_name": chapter_name,
            "quiz_titles": list(quiz_titles)
        }
        return json.dumps(result)

    except Chapter.DoesNotExist:
        return json.dumps({
            "error": "Chapter not found",
            "class_name": class_name,
            "subject_name": subject_name,
            "chapter_name": chapter_name
        })


def book(request, classname, subjectname, chapter_name,rec):
    try:
        # Retrieve Class, Subject, and Chapter based on names
        class_instance = Class.objects.get(class_name=classname)
        subject_instance = Subject.objects.get(subject_name=subjectname, class_fk=class_instance)
        chapter_instance = Chapter.objects.get(chapter_name=chapter_name, subject_fk=subject_instance)
        resource = ChapterResource.objects.filter(chapter=chapter_instance).first()
    except Class.DoesNotExist:
        return JsonResponse({'error': 'Class not found'}, status=404)
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)
    except Chapter.DoesNotExist:
        return JsonResponse({'error': 'Chapter not found'}, status=404)
    
    # Prepare data with URLs
    data = {
        
        'chapter_name':chapter_name,
        'subject_name' :subjectname,
        'class_name': classname,
        'english_book_url': resource.english_book_file.url if resource and resource.english_book_file else None,
        'hindi_book_url': resource.hindi_book_file.url if resource and resource.hindi_book_file else None,
        "notes":resource.notes_file.url if resource and resource.notes_file else None,
        'mindmap_pdf_url':resource.mind_map.url if resource and resource.mind_map else None,
        'ncert_sol_pdf_url' : resource.ncert_sol_file.url if resource and resource.ncert_sol_file else None    }
    if(rec=="notes"):
        return render(request,"notes.html",data)
    if(rec=="mindmap"):
        return render(request,"mindmap.html",data)
    elif(rec=="eng-book"):
        return render(request,"book.html",data)
    elif(rec=="hin-book"):
        return render(request,"hin-book.html",data)
    elif(rec=="ncert-sol"):
        return render (request,"ncertsol.html",data)


def classes(request, class_name):
    # Retrieve the class instance based on the provided class_name
    try:
        class_instance = Class.objects.get(class_name=class_name)
    except Class.DoesNotExist:
        raise Http404("Class not found")
    
    # Retrieve all subjects related to this class
    subjects = Subject.objects.filter(class_fk=class_instance)
    
    # Pass the class instance and subjects to the template context
    context = {
        'class_instance': class_instance,
        'subjects': subjects,
    }
    return render(request, 'classes.html', context)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

