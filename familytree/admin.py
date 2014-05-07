import sys
from familytree.models import FamilyMember, Marriage
from django.contrib import admin

class DescendantInline(admin.TabularInline):
    model = Marriage
    fk_name = 'in_law'
    verbose_name = 'Spouse Descendant (Bloodline)'
    extra = 0
    
class InLawInline(admin.TabularInline):
    model = Marriage
    fk_name = 'descendant'
    verbose_name = 'Spouse In-Law (Non Bloodline)'
    extra = 0

class FamilyMemberAdmin(admin.ModelAdmin): 

    fieldsets = [
        ('Name',           {'fields': [('first_name','middle_name','last_name'),('maiden_name','preferred_name','ordinal')]}),
        ('Personal Info', {'fields': ['sex',('date_birth_date','string_birth_date'),('birth_city','birth_state','birth_country'),('date_death_date','string_death_date'),('death_city','death_state','death_country'),'bio','picture'],'classes' : ['']}),
        ('Relationships',  {'fields': ['parents','children'], 'classes': ['']})
    ]    
    inlines = [DescendantInline, InLawInline]
    filter_horizontal = ('parents','children')
    list_display = ['display_name','pk','picture']
    list_editable = ['picture']
    list_filter = ['last_name']
    search_fields = ['first_name','middle_name','last_name','maiden_name','preferred_name']
    
class MarriageAdmin(admin.ModelAdmin): 

    list_display = ['marriage_title','date_marriage_date','string_marriage_date','marriage_city','marriage_state','marriage_country','is_active']
    list_editable = ['date_marriage_date','string_marriage_date','marriage_city','marriage_state','marriage_country','is_active']
    search_fields = ['descendant__first_name','descendant__middle_name','descendant__last_name','descendant__maiden_name','descendant__preferred_name',
                     'in_law__first_name','in_law__middle_name','in_law__last_name','in_law__maiden_name','in_law__preferred_name']

admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Marriage, MarriageAdmin)