from django.contrib import admin


from .models import person,req_made,loc

class ContactAdmin(admin.ModelAdmin):
  list_display = ('user_id', 'username', 'phelped', 'phone', 'aadhar','photo','last_loc','verified','avg_rating')
  list_display_links = ('user_id', 'username')
  search_fields = ('username', 'phone', 'aadhar')
  list_per_page = 25

admin.site.register(person, ContactAdmin)


class ReqAdmin(admin.ModelAdmin):
  list_display = ('req_id','user_id','req_type','status','username', 'req_time','nprespond', 'location','auth_resp')
  list_display_links = ('req_id', 'username')
  search_fields = ('username', 'location', 'req_type')
  list_per_page = 25

admin.site.register(req_made, ReqAdmin)

class LocAdmin(admin.ModelAdmin):
  list_display = ('user_id','last_loc')
  list_display_links = ('user_id','last_loc')
  search_fields = ('user_id','last_loc')
  list_per_page = 25

admin.site.register(loc, LocAdmin)


