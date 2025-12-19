# Troubleshooting script for ChatBoard WebSocket issues

Write-Host "🔍 ChatBoard WebSocket Troubleshooting" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check if server is running
Write-Host "1️⃣ Checking if Daphne server is running on port 8000..." -ForegroundColor Yellow
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "   ✅ Port 8000 is in use (likely Daphne is running)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Port 8000 is not in use (Daphne might not be running)" -ForegroundColor Red
    Write-Host "   💡 Start server with: python manage.py runserver" -ForegroundColor Blue
}

Write-Host ""

# 2. Check Python packages
Write-Host "2️⃣ Checking Python packages..." -ForegroundColor Yellow
python -c "
try:
    import channels
    print('   ✅ Django Channels installed')
except ImportError:
    print('   ❌ Django Channels not installed')
    
try:
    import daphne
    print('   ✅ Daphne installed')
except ImportError:
    print('   ❌ Daphne not installed')
    
try:
    import django_extensions
    print('   ✅ Django Extensions installed')
except ImportError:
    print('   ℹ️  Django Extensions not installed (optional)')
"

Write-Host ""

# 3. Database check
Write-Host "3️⃣ Database check..." -ForegroundColor Yellow
if (Test-Path "db.sqlite3") {
    Write-Host "   ✅ Database exists" -ForegroundColor Green
} else {
    Write-Host "   ❌ Database not found" -ForegroundColor Red
    Write-Host "   💡 Run: python manage.py migrate" -ForegroundColor Blue
}

Write-Host ""

# 4. Settings check
Write-Host "4️⃣ Checking Django settings..." -ForegroundColor Yellow
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatboard.settings')
try:
    django.setup()
    from django.conf import settings
    
    # Check ASGI Application
    if hasattr(settings, 'ASGI_APPLICATION'):
        print('   ✅ ASGI_APPLICATION:', settings.ASGI_APPLICATION)
    
    # Check Channel Layers
    if hasattr(settings, 'CHANNEL_LAYERS'):
        backend = settings.CHANNEL_LAYERS['default']['BACKEND']
        print('   ✅ CHANNEL_LAYERS backend:', backend)
    
    # Check Installed Apps
    if 'channels' in settings.INSTALLED_APPS:
        print('   ✅ Channels in INSTALLED_APPS')
    if 'chat' in settings.INSTALLED_APPS:
        print('   ✅ Chat app in INSTALLED_APPS')
        
except Exception as e:
    print('   ❌ Error checking settings:', str(e))
" 2>$null

Write-Host ""
Write-Host "📋 Quick Start Guide:" -ForegroundColor Cyan
Write-Host "1. Start server: python manage.py runserver" -ForegroundColor White
Write-Host "2. Go to: http://localhost:8000/dashboard/" -ForegroundColor White
Write-Host "3. Click a user to open chat" -ForegroundColor White
Write-Host "4. Press F12 to open DevTools" -ForegroundColor White
Write-Host "5. Go to Console tab" -ForegroundColor White
Write-Host "6. Type a message and click Send" -ForegroundColor White
Write-Host "7. Watch console for real-time logs" -ForegroundColor White

Write-Host ""
Write-Host "🐛 Debugging:" -ForegroundColor Cyan
Write-Host "- Check browser console (F12)" -ForegroundColor White
Write-Host "- Check Network tab for WebSocket connection" -ForegroundColor White
Write-Host "- Check server terminal for error messages" -ForegroundColor White
Write-Host "- Check that InMemoryChannelLayer is enabled in settings" -ForegroundColor White

Write-Host ""
Write-Host "✨ Common Issues:" -ForegroundColor Cyan
Write-Host "❓ WebSocket not connecting?" -ForegroundColor Yellow
Write-Host "   → Restart server and refresh page" -ForegroundColor White
Write-Host ""
Write-Host "❓ Message not being sent?" -ForegroundColor Yellow
Write-Host "   → Check browser console for errors" -ForegroundColor White
Write-Host "   → Make sure WebSocket state is 1 (OPEN)" -ForegroundColor White
Write-Host ""
Write-Host "❓ Database errors?" -ForegroundColor Yellow
Write-Host "   → Run: python manage.py migrate" -ForegroundColor White
