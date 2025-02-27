from django.contrib import admin
from .models import Class, Subject, Chapter, ChapterResource, Quiz, Worksheet, Questionsheet


admin.site.site_header = "Active Study Admin"  # Change the header
admin.site.site_title = "Active Study Admin Panel"  # Change the title
admin.site.index_title = "Welcome to Active Study Admin Dashboard"  # Change the index title

class BaseChapterAdmin(admin.ModelAdmin):
    def get_subject(self, obj):
        return obj.chapter.subject_fk.subject_name
    get_subject.short_description = 'Subject'

    def get_class(self, obj):
        return obj.chapter.subject_fk.class_fk.class_name
    get_class.short_description = 'Class'

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name',)
    search_fields = ('class_name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'class_fk')
    search_fields = ('subject_name', 'class_fk__class_name')
    list_filter = ('class_fk',)
    autocomplete_fields = ['class_fk']

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1
    fields = ('title', 'quiz_file')

class WorksheetInline(admin.TabularInline):
    model = Worksheet
    extra = 1
    fields = ('title', 'worksheet_file')  # Updated field name

class QuestionSheetInline(admin.TabularInline):
    model = Questionsheet
    extra = 1
    fields = ('title', 'question_sheet_file')  # Updated field name

class ChapterResourceInline(admin.TabularInline):
    model = ChapterResource
    extra = 1
    fields = ('notes_file', 'english_book_file', 'hindi_book_file', 'ncert_sol_file', 'mind_map')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'subject_fk', 'get_class')
    search_fields = ('chapter_name', 'subject_fk__subject_name')
    list_filter = ('subject_fk__class_fk', 'subject_fk')
    autocomplete_fields = ['subject_fk']
    inlines = [QuizInline, ChapterResourceInline, WorksheetInline, QuestionSheetInline]

    def get_class(self, obj):
        return obj.subject_fk.class_fk.class_name
    get_class.short_description = 'Class'

@admin.register(Quiz)
class QuizAdmin(BaseChapterAdmin):
    list_display = ('title', 'chapter', 'get_subject', 'get_class')
    search_fields = ('title', 'chapter__chapter_name')
    list_filter = ('chapter__subject_fk__class_fk', 'chapter__subject_fk')
    autocomplete_fields = ['chapter']

@admin.register(Worksheet)
class WorksheetAdmin(BaseChapterAdmin):
    list_display = ('title', 'chapter', 'get_subject', 'get_class')
    search_fields = ('title', 'chapter__chapter_name')
    list_filter = ('chapter__subject_fk__class_fk', 'chapter__subject_fk')
    autocomplete_fields = ['chapter']

@admin.register(Questionsheet)
class QuestionSheetAdmin(BaseChapterAdmin):
    list_display = ('title', 'chapter', 'get_subject', 'get_class')
    search_fields = ('title', 'chapter__chapter_name')
    list_filter = ('chapter__subject_fk__class_fk', 'chapter__subject_fk')
    autocomplete_fields = ['chapter']