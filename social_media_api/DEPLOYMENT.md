# Deployment Documentation

## Production Environment Configuration

### Required Environment Variables
```
SECRET_KEY=your-production-secret-key
DB_PASSWORD=your-database-password
DB_NAME=social_media_db
DB_USER=postgres
DB_HOST=your-database-host
DB_PORT=5432
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DEBUG=False
```

### Database Configuration
- **Engine**: PostgreSQL
- **Connection**: Environment variables
- **Migrations**: Auto-run on deployment

### Security Settings
- SSL redirect enabled
- Secure cookies enabled
- HSTS configured (1 year)
- XSS protection enabled
- Content type sniffing disabled

### Static Files
- **Storage**: WhiteNoise with compression
- **Collection**: Auto-collected on deployment
- **Path**: `/static/`

## Deployment Steps

### 1. Pre-deployment
```bash
# Update requirements
pip freeze > requirements.txt

# Test locally
python manage.py check --deploy
python manage.py collectstatic --noinput
```

### 2. Platform Deployment

#### DigitalOcean App Platform
```bash
# Build Command
cd social_media_api && pip install -r requirements.txt

# Run Command  
cd social_media_api && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn social_media_api.wsgi --log-file -
```

#### Railway
```bash
# Connect GitHub repo
# Add PostgreSQL database
# Set environment variables
# Deploy automatically
```

### 3. Post-deployment
```bash
# Create superuser
python manage.py createsuperuser

# Verify migrations
python manage.py showmigrations
```

## Production Checklist
- [ ] Environment variables set
- [ ] Database connected
- [ ] Static files serving
- [ ] SSL certificate active
- [ ] Admin panel accessible
- [ ] API endpoints responding
- [ ] Authentication working