#!/bin/bash
# Troubleshooting script for ChatBoard WebSocket issues

echo "🔍 ChatBoard WebSocket Troubleshooting"
echo "======================================"
echo ""

# Check if server is running
echo "1️⃣ Checking if Daphne server is running on port 8000..."
if netstat -an | grep -q ":8000 " 2>/dev/null; then
    echo "   ✅ Port 8000 is in use (likely Daphne is running)"
else
    echo "   ❌ Port 8000 is not in use (Daphne might not be running)"
    echo "   💡 Start server with: python manage.py runserver"
fi

echo ""
echo "2️⃣ Checking Python packages..."
python -c "
try:
    import channels
    print('   ✅ Django Channels:', channels.__version__)
except:
    print('   ❌ Django Channels not installed')
    
try:
    import daphne
    print('   ✅ Daphne:', daphne.__version__)
except:
    print('   ❌ Daphne not installed')
" 2>/dev/null

echo ""
echo "3️⃣ Database check..."
if [ -f "db.sqlite3" ]; then
    echo "   ✅ Database exists"
else
    echo "   ❌ Database not found"
    echo "   💡 Run: python manage.py migrate"
fi

echo ""
echo "4️⃣ Testing WebSocket configuration..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatboard.settings')
django.setup()

from django.conf import settings
if hasattr(settings, 'CHANNEL_LAYERS'):
    print('   ✅ CHANNEL_LAYERS configured')
    if 'default' in settings.CHANNEL_LAYERS:
        backend = settings.CHANNEL_LAYERS['default']['BACKEND']
        print(f'   📌 Using backend: {backend}')
else:
    print('   ❌ CHANNEL_LAYERS not configured')
" 2>/dev/null

echo ""
echo "📋 Next steps:"
echo "1. Make sure server is running: python manage.py runserver"
echo "2. Go to http://localhost:8000/dashboard/"
echo "3. Click on a user to open chat"
echo "4. Press F12 to open DevTools"
echo "5. Go to Console tab"
echo "6. You should see: '✅ Chat Configuration:'"
echo "7. Type a message and click Send"
echo "8. Watch console for logs"
echo ""
echo "💡 If still not working, check:"
echo "   - Terminal output for errors"
echo "   - Browser console (F12) for errors"
echo "   - WebSocket tab in Network panel"
echo ""
