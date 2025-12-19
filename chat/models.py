"""
Database models for chat application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class UserProfile(models.Model):
    """Extended user profile for additional features"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Profile"

    class Meta:
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Message(models.Model):
    """Model to store chat messages between users"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=True)  # True = delivered, False = pending
    read_at = models.DateTimeField(null=True, blank=True)  # When message was read
    file_attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)  # File/Image
    file_name = models.CharField(max_length=255, null=True, blank=True)  # Original filename
    file_type = models.CharField(max_length=50, null=True, blank=True)  # mime type
    
    # Media type: 'text', 'image', 'video', 'audio', 'document'
    media_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('audio', 'Audio'),
            ('document', 'Document'),
        ],
        default='text'
    )
    
    # Security & Control
    is_deleted = models.BooleanField(default=False)  # Soft delete
    deleted_for_me = models.BooleanField(default=False)  # Delete for sender only
    deleted_for_recipient = models.BooleanField(default=False)  # Delete for receiver only
    is_encrypted = models.BooleanField(default=True)  # End-to-end encryption flag

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver', 'timestamp']),
            models.Index(fields=['receiver', 'is_read']),
        ]

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    def read_message(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save()
            self.is_read = True
            self.save()


class BlockedUser(models.Model):
    """Model to manage blocked users"""
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('blocker', 'blocked_user')
        verbose_name_plural = "Blocked Users"

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked_user.username}"


class ReportedUser(models.Model):
    """Model to store user reports"""
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.CharField(
        max_length=255,
        choices=[
            ('spam', 'Spam'),
            ('harassment', 'Harassment'),
            ('inappropriate', 'Inappropriate Content'),
            ('fake_account', 'Fake Account'),
            ('other', 'Other'),
        ]
    )
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reporter', 'reported_user')
        verbose_name_plural = "Reported Users"

    def __str__(self):
        return f"{self.reporter.username} reported {self.reported_user.username}"


class UserPrivacySettings(models.Model):
    """Model for user privacy preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privacy_settings')
    
    # Message privacy
    allow_read_receipts = models.BooleanField(default=True)  # Show when messages are read
    allow_typing_status = models.BooleanField(default=True)  # Show typing indicator
    allow_last_seen = models.BooleanField(default=True)  # Show last seen status
    
    # Contact privacy
    allow_unknown_messages = models.BooleanField(default=False)  # Allow messages from non-contacts
    
    # Media sharing
    auto_download_media = models.BooleanField(default=True)  # Auto-download images/videos
    allow_media_sharing = models.BooleanField(default=True)  # Allow other users to share media
    
    # Profile visibility
    show_profile_picture = models.BooleanField(default=True)
    show_bio = models.BooleanField(default=True)
    show_phone_number = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Privacy Settings for {self.user.username}"

    class Meta:
        verbose_name_plural = "User Privacy Settings"


@receiver(post_save, sender=User)
def create_user_privacy_settings(sender, instance, created, **kwargs):
    """Automatically create UserPrivacySettings when a User is created"""
    if created:
        UserPrivacySettings.objects.create(user=instance)
