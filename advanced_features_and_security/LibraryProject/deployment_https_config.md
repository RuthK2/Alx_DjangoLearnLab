# HTTPS Deployment Configuration

## Overview
This document provides instructions for configuring your web server to support HTTPS with SSL/TLS certificates for the Django LibraryProject application.

## Prerequisites
- SSL/TLS certificate (from Let's Encrypt, commercial CA, or self-signed for testing)
- Web server (Nginx or Apache)
- Domain name pointing to your server

## Nginx Configuration

### 1. Basic HTTPS Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificate Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/your/static/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Apache Configuration

### 1. Enable Required Modules
```bash
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod headers
```

### 2. Virtual Host Configuration
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key
    SSLCertificateChainFile /path/to/your/chain.crt

    # SSL Security
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305
    SSLHonorCipherOrder off

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"

    # Django Application
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPreserveHost On
    ProxyAddHeaders On
</VirtualHost>
```

## Let's Encrypt SSL Certificate Setup

### 1. Install Certbot
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

### 2. Obtain Certificate
```bash
# For Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For Apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

### 3. Auto-renewal Setup
```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab for automatic renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## Environment Variables for Production

Set these environment variables in your production environment:

```bash
export DEBUG=False
export SECURE_SSL_REDIRECT=True
export SECURE_HSTS_SECONDS=31536000
export SECURE_HSTS_INCLUDE_SUBDOMAINS=True
export SECURE_HSTS_PRELOAD=True
export SESSION_COOKIE_SECURE=True
export CSRF_COOKIE_SECURE=True
```

## Testing HTTPS Configuration

### 1. SSL Labs Test
Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com

### 2. Security Headers Test
Visit: https://securityheaders.com/?q=yourdomain.com

### 3. Django Check
```bash
python manage.py check --deploy
```

## Troubleshooting

### Common Issues:
1. **Mixed Content Warnings**: Ensure all resources (CSS, JS, images) use HTTPS URLs
2. **Certificate Chain Issues**: Verify intermediate certificates are properly configured
3. **HSTS Not Working**: Check that headers are being sent correctly
4. **Redirect Loops**: Ensure proxy headers are configured properly

### Debug Commands:
```bash
# Check certificate
openssl x509 -in certificate.crt -text -noout

# Test SSL connection
openssl s_client -connect yourdomain.com:443

# Check headers
curl -I https://yourdomain.com
```