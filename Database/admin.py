from django.contrib import admin
from Database.models import Employee,RoomType,Room,Guest,Booking,Service,BookingService
admin.site.register(Employee)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Service)
admin.site.register(BookingService)
