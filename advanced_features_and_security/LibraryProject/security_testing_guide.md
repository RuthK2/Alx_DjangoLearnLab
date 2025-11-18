# Security Testing Guide

## 1. Local Testing Commands

### Django Built-in Security Check
```bash
cd LibraryProject
python manage.py check --deploy
```

### Run Security Test Script
```bash
python test_security.py
```

### Test with Different DEBUG Settings
```bash
# Test in development mode (DEBUG=True)
set DEBUG=True
python test_security.py

# Test in production mode (DEBUG=False)
set DEBUG=False
python test_security.py
```

## 2. Manual Header Testing

### Using curl (if available)
```bash
# Test HTTP redirect
curl -I http://localhost:8000/

# Test HTTPS headers
curl -I -k https://localhost:8000/
```

### Using PowerShell
```powershell
# Test HTTP response
Invoke-WebRequest -Uri "http://localhost:8000/" -Method Head

# Test with HTTPS simulation
$headers = @{'X-Forwarded-Proto' = 'https'}
Invoke-WebRequest -Uri "http://localhost:8000/" -Headers $headers -Method Head
```

## 3. Browser Testing

### Developer Tools Method
1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Visit your site
4. Check Response Headers for:
   - `X-Frame-Options: DENY`
   - `X-Content-Type-Options: nosniff`
   - `X-XSS-Protection: 1; mode=block`
   - `Strict-Transport-Security` (in production)

### Security Headers Checklist
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Strict-Transport-Security (production only)
- [ ] HTTP redirects to HTTPS (production only)

## 4. Online Security Testing Tools

### SSL Labs (for deployed sites)
- URL: https://www.ssllabs.com/ssltest/
- Tests SSL/TLS configuration
- Provides security grade (A+ is best)

### Security Headers (for deployed sites)
- URL: https://securityheaders.com/
- Tests HTTP security headers
- Provides security score

### Mozilla Observatory (for deployed sites)
- URL: https://observatory.mozilla.org/
- Comprehensive security analysis
- Provides recommendations

## 5. Production Testing Steps

### Before Deployment
1. Run `python manage.py check --deploy`
2. Test with `DEBUG=False` locally
3. Verify all security settings are enabled

### After Deployment
1. Test SSL certificate: `openssl s_client -connect yourdomain.com:443`
2. Check headers: `curl -I https://yourdomain.com`
3. Run online security scanners
4. Verify HSTS is working
5. Test HTTP to HTTPS redirect

## 6. Expected Results

### Development Mode (DEBUG=True)
- SECURE_SSL_REDIRECT: False
- SECURE_HSTS_SECONDS: 0
- SESSION_COOKIE_SECURE: False
- CSRF_COOKIE_SECURE: False
- No HTTPS redirects
- Basic security headers still active

### Production Mode (DEBUG=False)
- SECURE_SSL_REDIRECT: True
- SECURE_HSTS_SECONDS: 31536000
- SESSION_COOKIE_SECURE: True
- CSRF_COOKIE_SECURE: True
- HTTP redirects to HTTPS
- Full security headers active

## 7. Troubleshooting

### Common Issues
1. **Mixed Content**: Ensure all resources use HTTPS
2. **Redirect Loops**: Check proxy configuration
3. **Headers Not Showing**: Verify middleware order
4. **HSTS Not Working**: Check browser cache/incognito mode

### Debug Commands
```bash
# Check current settings
python manage.py shell -c "from django.conf import settings; print(settings.SECURE_SSL_REDIRECT)"

# Test specific view
python manage.py shell -c "from django.test import Client; c = Client(); print(c.get('/').status_code)"
```