# Online Status - Quick Reference Guide

## 🚀 Getting Started

### Access the Feature
1. Login to ChatBoard
2. Click "Online status" on dashboard
3. Or navigate to: `/online-status/`

### Main Actions
- **Search**: Type name or username in search box
- **Filter**: Click status button (Online, Offline, Away, Busy)
- **Message**: Click "Message" button to chat
- **Profile**: Click "Profile" button (coming soon)

---

## 📊 Understanding the Status Page

### Header Section
```
ChatBoard | Welcome, username! | Dashboard | Logout
```

### Statistics Cards
```
[5 Online] [8 Offline] [2 Away] [1 Busy]
```
Shows real-time count of users in each status.

### Search & Filters
```
[Search box] [All] [Online] [Offline] [Away] [Busy]
```
- Type to search instantly
- Click filter to view specific status
- Active filter is highlighted in purple

### User Grid
Cards display:
- **Avatar**: Initials in purple circle with status dot
- **Name & username**: User identification
- **Status badge**: Current availability status
- **Last seen**: When user was last active
- **Joined**: Account creation date
- **Messages**: Total messages sent by user
- **Action buttons**: Message and Profile buttons

---

## 🎨 Status Colors & Meanings

| Status | Color | Indicator | Meaning |
|--------|-------|-----------|---------|
| Online | 🟢 Green | Solid green dot | User is active |
| Offline | ⚫ Gray | Solid gray dot | User is inactive |
| Away | 🟡 Yellow | Solid yellow dot | User is idle |
| Busy | 🔴 Red | Solid red dot | User is busy |

---

## ⚙️ Features & Capabilities

### ✅ Search
- Real-time filtering as you type
- Searches by full name
- Searches by username
- Case-insensitive matching

### ✅ Filter
- All Users - Shows everyone
- Online - Shows active users
- Offline - Shows inactive users
- Away - Shows idle users
- Busy - Shows busy users

### ✅ Statistics
- Updates automatically
- Shows count of each status
- Updates every 3 seconds

### ✅ User Cards
- Shows essential information
- Professional layout
- Hover effects
- Quick action buttons

### ✅ Auto-Refresh
- Updates every 3 seconds
- No manual refresh needed
- Seamless background updates

---

## 💡 Tips & Tricks

### Search Tips
- Search by first name: "John"
- Search by last name: "Doe"
- Search by username: "johndoe"
- Search is case-insensitive

### Filter Tips
- Click a filter to activate it
- Click another filter to switch
- All other filters are deactivated
- Click "All Users" to reset

### Card Information
- **Last Seen**: Shows when user was last active
- **Joined**: Shows account creation date
- **Messages**: Shows total messages sent by user

### Quick Navigation
- Message button → Opens direct chat with user
- Profile button → View user profile (future)
- Back to dashboard → Click "Dashboard" in header

---

## 🔄 Auto-Update Information

### What Updates
- User status (online/offline)
- Statistics counters
- User card display
- Search results

### Update Frequency
- Every 3 seconds automatically
- No action required
- Works in background

### How It Works
1. Page loads user data
2. Displays on screen
3. Waits 3 seconds
4. Fetches fresh data
5. Updates display
6. Repeats

---

## 🚨 Common Issues & Solutions

### Problem: Users not showing
**Solution**: Ensure at least 1 other user is registered in system

### Problem: Search not working
**Solution**: 
- Check spelling
- Try different search terms
- Make sure user exists

### Problem: Filters not working
**Solution**:
- Refresh the page
- Check browser console for errors
- Try clearing browser cache

### Problem: Status not updating
**Solution**:
- Wait for 3-second auto-refresh
- Reload the page
- Check internet connection

### Problem: Can't message user
**Solution**:
- Ensure you're logged in
- Check if user exists
- Try refreshing page

---

## 🎯 Use Cases

### Find Active Users
1. Click "Online" filter
2. See all currently active users
3. Message someone available

### Search Specific User
1. Type username in search
2. User card appears if online
3. Click "Message" to chat

### Check When User Last Seen
1. Find user in list
2. Look at "Last Seen" date
3. See when they were last active

### See Account Join Date
1. Find user in list
2. Look at "Joined" date
3. See when they created account

### Check User Activity
1. Find user in list
2. Look at "Messages" count
3. See total messages sent

---

## 🔐 Privacy & Security

### What You Can See
- User name and username
- Current status
- Join date
- Last seen date
- Message count

### What You Can't See
- User's password
- User's email
- Private messages
- Personal information
- Phone number

### Privacy Settings
Users can control what you see in settings (future feature)

---

## 📱 Mobile & Responsive Design

### Mobile Devices
- Page optimized for phones
- Single column layout
- Touch-friendly buttons
- Easy scrolling

### Tablets
- 2-column layout
- Medium-sized cards
- Comfortable spacing

### Desktop
- 4-column grid layout
- Large cards
- Full information display

### Adjust for Your Device
- Landscape orientation - shows more columns
- Portrait orientation - shows single column
- Responsive at all sizes

---

## 🔗 Related Features

### Connected Pages
- **Dashboard** - Main hub, access via header button
- **Chat** - Message other users, click "Message" button
- **AI Chat** - Chat with AI assistant, access from dashboard

### Database Connected
- User accounts and profiles
- Message history
- User status tracking
- Activity timestamps

---

## ⏱️ Time-Based Information

### Last Seen
Shows how long since user was active
- Real-time: "5 minutes ago"
- Historical: "2 days ago"
- Never: "Never" (new accounts)

### Joined Date
Shows when account was created
- Format: "January 1, 2025"
- Allows you to see user tenure
- Helps identify new vs. old accounts

---

## 📈 Understanding Statistics

### Online Count
- Users currently active
- Green status indicator
- Refreshes every 3 seconds

### Offline Count
- Users not currently active
- Gray status indicator
- Includes idle users

### Away Count
- Users marked as away
- Yellow status indicator
- Indicates idle status

### Busy Count
- Users marked as busy
- Red status indicator
- Indicates unavailable status

---

## 🎓 Learning Resources

### Want to Learn More?
- **Full Documentation**: ONLINE_STATUS_FEATURE.md
- **Code Implementation**: ONLINE_STATUS_SUMMARY.md
- **Main README**: README.md
- **Quick Start**: START_HERE.md

### Developer References
- **Backend Code**: chat/views.py
- **URL Routes**: chat/urls.py
- **Database Models**: chat/models.py
- **Template**: templates/online_status.html

---

## ✨ Feature Highlights

✅ Real-time status updates  
✅ Powerful search capabilities  
✅ Multiple filtering options  
✅ Beautiful card-based design  
✅ Mobile responsive  
✅ Auto-refresh every 3 seconds  
✅ Quick message access  
✅ Statistics dashboard  
✅ No technical knowledge required  
✅ Fully secure & private  

---

## 📞 Need Help?

### Check These First
1. Is someone else logged in?
2. Is your internet connection working?
3. Have you tried refreshing the page?
4. Check browser console for errors

### Documentation
- Read ONLINE_STATUS_FEATURE.md for details
- Review this guide for quick answers
- Check README.md for general help

---

**Last Updated**: December 19, 2025  
**Version**: 1.0  
**Status**: ✅ READY TO USE
