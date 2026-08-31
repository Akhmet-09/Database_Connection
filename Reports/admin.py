from django.contrib import admin
from .models import BorrowRecord,Book,Member
class BorrowwRecordAdmin(admin.ModelAdmin):
    list_display = ['book','member','is_returned','borrow_date']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','publication_year','rating',]

class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership_type','total_borrowed']


admin.site.register(BorrowRecord,BorrowwRecordAdmin)
admin.site.register(Member,MemberAdmin)
admin.site.register(Book,BookAdmin)