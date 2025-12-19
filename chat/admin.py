"""
Admin configuration for chat app.
"""
from django.contrib import admin
from .models import UserProfile, Message, BlockedUser, ReportedUser, UserPrivacySettings


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_online', 'created_at')
    list_filter = ('is_online', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'media_type', 'timestamp', 'is_read', 'is_deleted')
    list_filter = ('timestamp', 'is_read', 'is_deleted', 'media_type', 'is_encrypted')
    search_fields = ('sender__username', 'receiver__username', 'message_text')
    readonly_fields = ('id', 'timestamp', 'sender', 'receiver')
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Message Content', {
            'fields': ('id', 'sender', 'receiver', 'message_text', 'media_type', 'file_attachment', 'file_name', 'file_type')
        }),
        ('Status', {
            'fields': ('is_read', 'is_delivered', 'read_at', 'timestamp')
        }),
        ('Security & Control', {
            'fields': ('is_deleted', 'deleted_for_me', 'deleted_for_recipient', 'is_encrypted')
        }),
    )


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ('blocker', 'blocked_user', 'timestamp', 'reason')
    list_filter = ('timestamp',)
    search_fields = ('blocker__username', 'blocked_user__username')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('Block Information', {
            'fields': ('blocker', 'blocked_user', 'reason', 'timestamp')
        }),
    )


@admin.register(ReportedUser)
class ReportedUserAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'reason', 'timestamp', 'is_resolved')
    list_filter = ('timestamp', 'reason', 'is_resolved')
    search_fields = ('reporter__username', 'reported_user__username', 'description')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('Report Information', {
            'fields': ('reporter', 'reported_user', 'reason', 'description')
        }),
        ('Status', {
            'fields': ('is_resolved', 'timestamp')
        }),
    )


@admin.register(UserPrivacySettings)
class UserPrivacySettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'allow_read_receipts', 'allow_typing_status', 'allow_last_seen', 'updated_at')
    list_filter = ('allow_read_receipts', 'allow_typing_status', 'allow_last_seen', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Message Privacy', {
            'fields': ('allow_read_receipts', 'allow_typing_status', 'allow_last_seen')
        }),
        ('Contact & Media Privacy', {
            'fields': ('allow_unknown_messages', 'auto_download_media', 'allow_media_sharing')
        }),
        ('Profile Visibility', {
            'fields': ('show_profile_picture', 'show_bio', 'show_phone_number')
        }),
        ('Metadata', {
            'fields': ('updated_at',)
        }),
    )
