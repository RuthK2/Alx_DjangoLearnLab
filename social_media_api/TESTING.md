# Production Testing Guide

## Pre-Deployment Testing

### 1. Local Production Simulation
```bash
# Set production environment
set DEBUG=False
set SECRET_KEY=test-key
set DB_PASSWORD=your-password

# Run checks
python manage.py check --deploy
python manage.py test
```

### 2. Security Testing
```bash
# Check security settings
python manage.py check --deploy --settings=social_media_api.settings

# Test SSL redirect (if enabled)
curl -I http://your-domain.com
```

## Post-Deployment Testing

### 1. API Endpoints Testing
```bash
# Health check
curl https://your-domain.com/

# Authentication
curl -X POST https://your-domain.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# Posts API
curl -H "Authorization: Token your-token" \
  https://your-domain.com/api/posts/
```

### 2. Admin Panel Testing
- Navigate to `/admin/`
- Login with superuser credentials
- Verify all models accessible
- Test CRUD operations

### 3. Database Testing
```bash
# Check migrations
python manage.py showmigrations

# Test database connection
python manage.py dbshell
```

### 4. Static Files Testing
- Check `/static/admin/` loads correctly
- Verify CSS/JS files accessible
- Test media file uploads

## Performance Testing
```bash
# Load testing (optional)
pip install locust
locust -f locustfile.py --host=https://your-domain.com
```

## Monitoring Checklist
- [ ] Application starts successfully
- [ ] Database connections working
- [ ] API responses under 2 seconds
- [ ] No 500 errors in logs
- [ ] SSL certificate valid
- [ ] All endpoints return expected responses
- [ ] File uploads working
- [ ] Email notifications sending (if configured)