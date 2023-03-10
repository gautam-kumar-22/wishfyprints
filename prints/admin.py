from django.contrib import admin
from .models import *


class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'absolute_url', 'has_submenu', 'rank', 'status']


class SubmenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'absolute_url', 'status']


class ValidPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'office_time', 'office_day']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'info_email', 'address']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['page', 'heading']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    prepopulated_fields = {'slug': ('title',)}


class IndustryAdmin(admin.ModelAdmin):
    list_display = ['menu', 'title']
    prepopulated_fields = {'slug': ('title',)}


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'sub_title', 'tag', 'status']
    prepopulated_fields = {'slug': ('title',)}


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'tags', 'status', 'creation_date']
    prepopulated_fields = {'slug': ('title',)}


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['heading', 'project_done', 'satisfied_clients']


class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['type', 'category_discount', 'available_quantity', 'status']
    prepopulated_fields = {'slug': ('type',)}

    def category_discount(self, obj):
        return str(obj.discount) + "%"


class PhotoAdmin(admin.StackedInline):
    model = Photo


class AdditionalInformationAdmin(admin.StackedInline):
    model = AdditionalInformation


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin, AdditionalInformationAdmin]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'price', 'discount', 'status']

    def discount(self, obj):
        return str(obj.category.discount) + "%"

    class Meta:
        model = Product


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'status']


class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'status']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject']


admin.site.register(Menu, MenuAdmin)
admin.site.register(Submenu, SubmenuAdmin)
# admin.site.register(ValidPage, ValidPageAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Service, ServiceAdmin)
# admin.site.register(Industry, IndustryAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Technology, TechnologyAdmin)
# admin.site.register(Blog, BlogAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Features, FeaturesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo)
admin.site.register(Product, ProductAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
