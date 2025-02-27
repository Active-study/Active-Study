
from django.db import models
import os

def resource_upload_path(instance, filename):
    chapter = instance.chapter  # Now using consistent 'chapter' attribute
    class_name = chapter.subject_fk.class_fk.class_name.lower().replace(" ", "_")
    subject_name = chapter.subject_fk.subject_name.lower().replace(" ", "_")
    chapter_name = chapter.chapter_name.lower().replace(" ", "_")
    return os.path.join(class_name, subject_name, chapter_name, filename)

class Class(models.Model):
    class_name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.class_name

class Subject(models.Model):
    class_fk = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subjects")
    subject_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.class_fk.class_name} - {self.subject_name}"

class Chapter(models.Model):
    subject_fk = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="chapters")
    chapter_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.subject_fk.subject_name} - {self.chapter_name}"

def delete_file(file_field):
    """Delete the file from storage if it exists."""
    if file_field and file_field.name and os.path.isfile(file_field.path):
        os.remove(file_field.path)

class Quiz(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="quizzes")
    quiz_file = models.FileField(upload_to=resource_upload_path)
    title = models.CharField(max_length=200, blank=True)
    def delete(self, *args, **kwargs):
        delete_file(self.quiz_file)
        super().delete(*args, **kwargs)
    def __str__(self):
        return f"Quiz {self.title} for {self.chapter.chapter_name}"

class Questionsheet(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="question_sheets")
    question_sheet_file = models.FileField(upload_to=resource_upload_path)  # Renamed field
    title = models.CharField(max_length=200, blank=True)
    def delete(self, *args, **kwargs):
        delete_file(self.question_sheet_file)
        super().delete(*args, **kwargs)
    def __str__(self):
        return f"Question Sheet {self.title} for {self.chapter.chapter_name}"

class Worksheet(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="worksheets")
    worksheet_file = models.FileField(upload_to=resource_upload_path)  # Renamed field
    title = models.CharField(max_length=200, blank=True)
    def delete(self, *args, **kwargs):
        delete_file(self.worksheet_file)
        super().delete(*args, **kwargs)
    def __str__(self):
        return f"Worksheet {self.title} for {self.chapter.chapter_name}"

class ChapterResource(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="resources")  # Renamed FK
    notes_file = models.FileField(upload_to=resource_upload_path, blank=True, null=True)
    english_book_file = models.FileField(upload_to=resource_upload_path, blank=True, null=True)
    hindi_book_file = models.FileField(upload_to=resource_upload_path, blank=True, null=True)
    ncert_sol_file = models.FileField(upload_to=resource_upload_path, blank=True, null=True)
    mind_map = models.FileField(upload_to=resource_upload_path, blank=True, null=True)
    
    def __str__(self):
        return f"Resources for {self.chapter.chapter_name}"
    
    def delete(self, *args, **kwargs):
        delete_file(self.notes_file)
        delete_file(self.english_book_file)
        delete_file(self.hindi_book_file)
        delete_file(self.ncert_sol_file)
        delete_file(self.mind_map)
        super().delete(*args, **kwargs)
