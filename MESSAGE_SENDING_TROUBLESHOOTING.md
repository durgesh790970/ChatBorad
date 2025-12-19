# Message Sending Troubleshooting Guide

## समस्या
Message send नहीं हो रहा है (Message is not being sent)

## समाधान के Steps

### 1️⃣ Server Check करें
```bash
# Terminal में check करें कि server चल रहा है
# Expected output:
# Starting ASGI/Daphne version 4.0.0 development server at http://0.0.0.0:8000/
```

### 2️⃣ Browser Console में Debug करें
```javascript
// Browser में F12 दबाएं (DevTools खोलें)
// Console tab में जाएं
// यह paste करें:

// Status check करने के लिए:
window.debugChat.getStatus()

// Output देखें:
// {
//   app: ChatApplication {...},
//   socket: WebSocket {...},
//   socketState: 1,  // 1 = OPEN (अच्छा है)
//   states: {0: "CONNECTING", 1: "OPEN", 2: "CLOSING", 3: "CLOSED"}
// }
```

### 3️⃣ Test Message भेजें
```javascript
// Console में:
window.debugChat.testMessage('Hello test')

// या manually:
document.getElementById('messageInput').value = 'Test message';
window.chatApplication.sendMessage();
```

### 4️⃣ Expected Console Output

**Successful scenario:**
```
✅ Chat Configuration:
   Current User ID: 1
   Other User ID: 2
   WebSocket URL: ws://localhost:8000/ws/chat/2/

✅ Initializing ChatApplication...

🔌 Attempting WebSocket connection to: ws://localhost:8000/ws/chat/2/
✅ WebSocket OPEN - Connection successful!
Event listeners setup complete

📤 SendMessage called
  Message text: Hello test
  WebSocket state: 1 (0=CONNECTING, 1=OPEN, 2=CLOSING, 3=CLOSED)
📨 Sending payload: {"message":"Hello test"}
✅ Message sent successfully to server
```

## Common Issues & Fixes

### Issue 1: WebSocket Connection Failed
```
❌ WebSocket ERROR: 
   WebSocket is not open. Current state: CLOSED (3)
```

**Fix:**
- Server को restart करें
- Page को refresh करें
- Check करें कि URL सही है

### Issue 2: Message Form Not Found
```
❌ Message form not found!
❌ Message input not found!
```

**Fix:**
- Page को refresh करें
- Browser cache clear करें (Ctrl+Shift+Delete)
- DevTools reload करें (Ctrl+F5)

### Issue 3: Receiver Not Found
```
❌ Receiver not found: 2
```

**Fix:**
- Check करें कि दूसरा user exist करता है
- Dashboard से फिर से chat खोलें

### Issue 4: JSON Parse Error
```
❌ Error parsing WebSocket message
```

**Fix:**
- Browser console में error details देखें
- Server को restart करें

## Files जो Edit किए गए

### ✅ settings.py
- Channel Layer को InMemoryChannelLayer set किया (Redis की जरूरत नहीं)

### ✅ chat.js
- विस्तृत logging जोड़ी
- WebSocket state validation improve की
- Error handling बेहतर की

### ✅ consumers.py
- Connection और message receiving में logging जोड़ी
- Error handling improve की

### ✅ chat.html
- Debug tools add किए
- WebSocket configuration logging

## Quick Checklist

- [ ] Server चल रहा है (`python manage.py runserver`)
- [ ] WebSocket URL सही है (ws://localhost:8000/ws/chat/[id]/)
- [ ] Channels configured है
- [ ] Database migration run है
- [ ] Static files load हो रहे हैं

## Testing करने के लिए Manual Steps

1. **Dashboard खोलें**
   - http://localhost:8000/dashboard/

2. **किसी user पर click करें**
   - Chat page खुलेगा

3. **F12 खोलें** (DevTools)
   - Console tab में जाएं

4. **Type करें:**
   ```javascript
   window.debugChat.getStatus()
   ```

5. **socketState देखें:**
   - `1` = ✅ Connected (अच्छा है)
   - `0` = 🔄 Connecting (थोड़ा इंतजार करें)
   - `2` या `3` = ❌ Disconnected (restart करें)

6. **Message भेजें और देखें:**
   ```javascript
   window.debugChat.testMessage('Hello')
   ```

7. **Console में logs देखें** - सब कुछ ठीक है या कहां issue है

## Backend Logs Check करें

Terminal में where Daphne running है:

```
✅ WebSocket connecting: User=username, Other User ID=2, Room=chat_1_2
✅ WebSocket connection accepted for room: chat_1_2

📨 WebSocket message received: {"message":"Hello test"}
💬 Processing message: Hello test
✅ Receiver found: other_username
✅ Message saved to DB: ID=123
✅ Message broadcasted to room: chat_1_2
```

## Still Not Working?

अगर फिर भी काम नहीं हो रहा:

1. **Server restart करें:**
   ```bash
   # Terminal में Ctrl+C दबाएं
   python manage.py runserver
   ```

2. **Browser refresh करें:**
   ```
   Ctrl+F5 (Hard refresh)
   ```

3. **Browser DevTools clear करें:**
   ```
   F12 → Application → Clear All
   ```

4. **Different browser try करें:**
   - Chrome, Firefox, Edge

5. **Network tab देखें:**
   - DevTools → Network tab
   - WebSocket connection है या नहीं

## Production में

Settings.py में यह line है:
```python
# Production में Redis use करें:
'BACKEND': 'channels_redis.core.RedisChannelLayer',
```

---

**Last Updated:** Dec 16, 2025
**Status:** 🟡 Troubleshooting Mode
