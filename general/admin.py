from django.contrib import admin
from general.filters import AuthorFilter, PostFilter
from general.models import (
    User,
    Post,
    Comment,
    Reaction,
)
from django.contrib.auth.models import Group
from rangefilter.filters import DateRangeFilter
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    # fields = (
    #     "first_name",
    #     "last_name",
    #     "username",
    #     "password",
    #     "email",
    #     "is_staff",
    #     "is_superuser",
    #     "is_active",
    #     "date_joined",
    #     "last_login",
    # )
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    fieldsets = (
        (
            "Личные данные", {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            }
        ),
        (
            "Учетные данные", {
                "fields": (
                    "username",
                    "password",
                )
            }
        ),
        (
            "Статусы", {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            }
        ),
        (
            None, {
                "fields": (
                    "friends",
                )
            }
        ),
        (
            "Даты", {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            }
        )
    )
    search_fields = (
        "id",
        "title",
        "email",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        ("date_joined", DateRangeFilter),
    )
    

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "body",
        "created_at",
    )
    readonly_fields = (
        "created_at",
    )
    list_filter = (
        AuthorFilter,
        ("created_at", DateRangeFilter),
    )
    search_fields = (
        "title",
    )

    def get_body(self, obj):
        max_length = 64
        if len(obj.body) > max_length:
            return obj.body[:61] + "..."
        return obj.body
    
    get_body.short_description = 'body'

    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("commetns")


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "body",
        "author",
        "created_at",
        "post",
    )
    list_display_links = (
        "id",
        "body",
    )
    list_filter = (
        PostFilter,
        AuthorFilter,
    )


@admin.register(Reaction)
class ReactionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "value",
        "author",
        "post",
    )
    list_filter = (
        PostFilter,
        AuthorFilter,
        ("value", ChoiceDropdownFilter),
    )
    autocomplete_fields = (
        "author",
        "post",
    )


admin.site.unregister(Group)
