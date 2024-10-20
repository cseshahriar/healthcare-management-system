# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Slider, Speciality, Service, Item, Doctor, Expertize, Faq, Gallery,
    Contact, Feedback, Symptom, Subject, Degree, DoctorDegree
)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'caption',
        'slogan',
        'image',
        'phone_number',
        'service_page_url',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'name',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'title',
        'description',
        'thumbnail',
        'cover',
        'image1',
        'image2',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    raw_id_fields = ('items',)
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'title',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'user',
        'name',
        'doctor_id',
        'picture',
        'details',
        'present_hospital',
        'twitter',
        'facebook',
        'instagram',
        'division',
        'district',
        'post_code',
        'address',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
        'user',
        'speciality',
        'division',
        'district',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Expertize)
class ExpertizeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'name',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'question',
        'answer',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'title',
        'image',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
    )
    date_hierarchy = 'created_at'
    list_editable = ('order', 'is_active', 'is_deleted', )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'name',
        'email',
        'phone',
        'subject',
        'message',
        'response',
    )
    list_filter = (
        'created_user',
        'update_user',
        'deleted_user',
        'created_at',
        'is_active',
        'is_deleted',
        'response',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_editable = ('is_active', 'is_deleted', )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'name',
        'email',
        'phone',
        'message',
        'user',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_editable = ('is_active', 'is_deleted', )


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'created_at',
        'is_active',
        'is_deleted',
        'name',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_editable = ('is_active', 'is_deleted', )


admin.site.register(Subject)
admin.site.register(Degree)
admin.site.register(DoctorDegree)

admin.site.site_header = 'HMS Admin'
admin.site.site_title = 'HMS-System'
admin.site.index_title = 'HMS-System'
