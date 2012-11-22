# coding: utf-8
from django.contrib import admin
from todolist.models import List, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class ListAdmin(admin.ModelAdmin):
    inlines = [ItemInline, ]


admin.site.register(List, ListAdmin)
admin.site.register(Item)
