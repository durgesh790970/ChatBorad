# Media Sharing & Security Features Documentation

## Overview
This document outlines the newly implemented media sharing and security features for the ChatBoard chat application.

---

## 🎥 **Media Sharing Tools**

### 1. Image Upload
- **Functionality**: Users can upload and share images in conversations
- **Supported Formats**: JPG, PNG, GIF, WebP
- **Max File Size**: Configurable (default: 10MB)
- **Database Field**: `file_attachment`, `media_type='image'`
- **Features**:
  - Thumbnail preview in chat
  - Full-size image viewing
  - Progressive loading

### 2. Video Sharing
- **Functionality**: Share videos in conversations
- **Supported Formats**: MP4, WebM, OGG
- **Max File Size**: Configurable (default: 50MB)
- **Database Field**: `file_attachment`, `media_type='video'`
- **Features**:
  - Video preview
  - Streaming playback
  - Download option

### 3. Audio / Voice Notes 🎙
- **Functionality**: Record and share voice messages
- **Supported Formats**: MP3, WAV, M4A
- **Max File Size**: Configurable (default: 5MB)
- **Database Field**: `file_attachment`, `media_type='audio'`
- **Features**:
  - Voice recording directly in chat
  - Playback controls
  - Duration display
  - Waveform visualization

### 4. Document Upload
- **Functionality**: Share documents in conversations
- **Supported Formats**: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT
- **Max File Size**: Configurable (default: 25MB)
- **Database Field**: `file_attachment`, `media_type='document'`
- **Features**:
  - File preview (when possible)
  - Download with original name
  - File info display (size, type)
  - Document viewer integration

---

## 🔐 **Security & Control Tools**

### 1. End-to-End Encryption
- **Implementation**: 
  - `is_encrypted` flag on Message model
  - AES-256 encryption for messages
  - Keys stored securely per conversation
- **Features**:
  - Automatic encryption/decryption
  - Key exchange protocol (E2EE)
  - No server-side access to plaintext
  - Backward compatible with existing messages

### 2. Block / Report User
- **BlockedUser Model**:
  ```python
  - blocker: User (who is blocking)
  - blocked_user: User (who is blocked)
  - timestamp: DateTime
  - reason: CharField (optional)
  ```
- **ReportedUser Model**:
  ```python
  - reporter: User (who reports)
  - reported_user: User (who is reported)
  - reason: Choice field
  - description: TextField
  - is_resolved: BooleanField
  ```
- **Report Reasons**:
  - Spam
  - Harassment
  - Inappropriate Content
  - Fake Account
  - Other

- **Blocking Features**:
  - Prevent blocked users from sending messages
  - Hide conversations from blocked users
  - Hide profile information
  - Remove from contacts

### 3. Delete Message
- **Options**:
  - **Delete for me**: `deleted_for_me = True`
    - Message removed from sender's view only
    - Recipient still sees the message
  - **Delete for everyone**: `is_deleted = True`
    - Message removed from both parties
    - Timestamp and "Deleted" indicator shown
  - **Permanent deletion**: Database cleanup after retention period

- **Implementation**:
  ```python
  # Fields on Message model:
  - is_deleted: BooleanField (soft delete)
  - deleted_for_me: BooleanField (sender only)
  - deleted_for_recipient: BooleanField (recipient only)
  ```

- **Features**:
  - Time window for deletion (default: 1 hour)
  - Edit history preservation
  - Admin audit trail
  - Notification to recipient if applicable

### 4. Privacy Settings

#### UserPrivacySettings Model
```python
# Message Privacy
- allow_read_receipts: Boolean (Show when message is read)
- allow_typing_status: Boolean (Show typing indicator)
- allow_last_seen: Boolean (Show last seen status)

# Contact Privacy
- allow_unknown_messages: Boolean (Accept messages from non-contacts)

# Media Sharing
- auto_download_media: Boolean (Auto-download images/videos)
- allow_media_sharing: Boolean (Allow others to share media)

# Profile Visibility
- show_profile_picture: Boolean
- show_bio: Boolean
- show_phone_number: Boolean
```

#### Privacy Control Features
- **Read Receipts Control**:
  - Disable to hide when you've read messages
  - Recipients see "delivered" instead of "read"

- **Typing Indicator Control**:
  - Hide typing status from specific users
  - Prevent "is typing..." notifications

- **Last Seen Control**:
  - Hide last seen timestamp
  - Set to "Recently" instead of exact time

- **Media Auto-Download**:
  - Control automatic downloading
  - Save bandwidth on mobile
  - Manual download option always available

- **Profile Privacy**:
  - Hide profile picture from non-contacts
  - Hide bio information
  - Hide phone number

---

## 📱 **Frontend Implementation**

### Media Upload Interface
```html
<!-- File attachment button in message input -->
<button class="file-button" id="attachFileBtn">📎</button>

<!-- File input (hidden) -->
<input type="file" id="fileInput" />

<!-- File preview before sending -->
<div id="filePreview">
  <span id="previewText">File selected</span>
  <button id="removeFileBtn">✕</button>
</div>
```

### Message Display with Media
```html
<!-- Text message -->
<div class="message-bubble">
  <p class="message-text">Hello!</p>
  <span class="message-time">12:45</span>
</div>

<!-- Media message -->
<div class="message-bubble media">
  <img src="/media/..." alt="Shared image" />
  <!-- OR -->
  <video src="/media/..." controls></video>
  <!-- OR -->
  <audio src="/media/..." controls></audio>
  <!-- OR -->
  <a href="/media/...">Document.pdf</a>
</div>
```

### Security Controls Menu
```html
<!-- Right-click context menu on message -->
<div class="message-context-menu">
  <button class="context-menu-item">✓ Read Receipt: On</button>
  <button class="context-menu-item">🔒 Delete for me</button>
  <button class="context-menu-item danger">🗑️ Delete for everyone</button>
  <hr>
  <button class="context-menu-item">⚠️ Report Message</button>
</div>

<!-- User controls menu -->
<div class="user-menu">
  <button class="menu-item">📞 Block User</button>
  <button class="menu-item">⚠️ Report User</button>
  <button class="menu-item">⚙️ Privacy Settings</button>
</div>
```

---

## 🔧 **API Endpoints**

### Message Management
```
POST   /api/messages/           - Send message with file
DELETE /api/messages/{id}/      - Delete message
PATCH  /api/messages/{id}/      - Update message (delete for me)
POST   /api/messages/{id}/soft-delete/ - Delete for everyone
```

### User Management
```
POST   /api/blocked-users/      - Block user
DELETE /api/blocked-users/{id}/ - Unblock user
GET    /api/blocked-users/      - List blocked users

POST   /api/reported-users/     - Report user
GET    /api/reported-users/     - List (admin only)
PATCH  /api/reported-users/{id}/ - Resolve report (admin)
```

### Privacy Settings
```
GET    /api/privacy-settings/   - Get user privacy settings
PATCH  /api/privacy-settings/   - Update privacy settings
```

---

## 🚀 **Usage Examples**

### Upload Media
```javascript
// In chat.js
document.getElementById('attachFileBtn').addEventListener('click', () => {
  document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    displayFilePreview(file);
    chatApplication.fileToSend = file;
  }
});
```

### Send Media Message
```javascript
async function sendMediaMessage() {
  const formData = new FormData();
  formData.append('message_text', messageInput.value);
  formData.append('file', fileToSend);
  formData.append('media_type', detectMediaType(fileToSend));
  formData.append('other_user_id', otherUserId);
  
  const response = await fetch('/api/messages/', {
    method: 'POST',
    body: formData
  });
}
```

### Block User
```javascript
async function blockUser(userId) {
  const response = await fetch('/api/blocked-users/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      blocked_user: userId,
      reason: 'Harassment'
    })
  });
}
```

### Update Privacy Settings
```javascript
async function updatePrivacySettings() {
  const settings = {
    allow_read_receipts: false,
    allow_typing_status: false,
    allow_last_seen: false,
    auto_download_media: false
  };
  
  const response = await fetch('/api/privacy-settings/', {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(settings)
  });
}
```

---

## 📊 **Database Schema**

### New Tables
- `chat_blockeduser` - Stores blocked user relationships
- `chat_reporteduser` - Stores user reports
- `chat_userprivacysettings` - Stores user privacy preferences

### Modified Tables
- `chat_message` - Added:
  - `media_type` - Type of media (text, image, video, audio, document)
  - `is_deleted` - Soft delete flag
  - `deleted_for_me` - Deleted for sender only
  - `deleted_for_recipient` - Deleted for recipient only
  - `is_encrypted` - Encryption flag

---

## ⚡ **Performance Considerations**

### File Size Limits
- **Images**: 10 MB
- **Videos**: 50 MB
- **Audio**: 5 MB
- **Documents**: 25 MB

### Optimization
- Thumbnail generation for images
- Video transcoding for compatibility
- Compression for transmission
- CDN integration for media delivery

### Database
- Indexing on `media_type`, `timestamp`, `is_deleted`
- Soft deletes for data recovery
- Archive old files after 90 days

---

## 🛡️ **Security Best Practices**

1. **File Upload Security**:
   - Validate file types on server
   - Scan uploads for malware
   - Store outside webroot
   - Generate secure access tokens

2. **Encryption**:
   - Use TLS/SSL for transmission
   - Implement E2EE with AES-256
   - Key rotation every 30 days
   - Never store keys in plaintext

3. **User Privacy**:
   - Respect privacy settings
   - Audit access logs
   - Allow users to download their data
   - Comply with GDPR/CCPA

4. **Content Moderation**:
   - Auto-flag inappropriate content
   - Manual review queue
   - Escalation to admins
   - User blocking prevents contact

---

## 📝 **Notes**

- All features are designed to be backward compatible
- Privacy settings can be changed at any time
- Deleted messages can be recovered by admins (with audit trail)
- Media files are stored securely with access control
- User reports are reviewed by administrators

---

**Last Updated**: December 19, 2025
**Version**: 1.0
