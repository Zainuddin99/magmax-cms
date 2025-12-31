# Railway Deployment Guide for Backend

This guide will walk you through deploying your Django backend independently on Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your backend code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Railway CLI (optional, but helpful)

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure all the deployment files are committed to your repository:
- `Procfile` ✅
- `runtime.txt` ✅
- `requirements.txt` (updated with gunicorn and whitenoise) ✅
- `railway.json` ✅

### Step 2: Create a Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"** (or GitLab/Bitbucket)
4. Choose your repository
5. Railway will automatically detect it's a Python project

### Step 3: Configure the Service

1. Railway will create a service automatically
2. Click on the service to configure it
3. Go to **Settings** tab
4. Set the **Root Directory** to `backend` (since your backend code is in the backend folder)

### Step 4: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will create a PostgreSQL database
4. The database connection details will be automatically available as environment variables

### Step 5: Configure Environment Variables

Go to your service **Variables** tab and add the following environment variables:

#### Required Variables:

```
SECRET_KEY=your-very-secure-secret-key-here-generate-a-random-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,*.railway.app
```

#### Database Variables (Railway provides these automatically, but verify):

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=${{Postgres.DATABASE}}
DB_USER=${{Postgres.USER}}
DB_PASSWORD=${{Postgres.PASSWORD}}
DB_HOST=${{Postgres.HOST}}
DB_PORT=${{Postgres.PORT}}
```

**Note:** Railway automatically provides database connection variables. You can reference them using `${{Postgres.VARIABLE_NAME}}` syntax.

#### CORS Settings (Update with your frontend URL):

```
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

#### Media Files (Optional - for file uploads):

```
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

### Step 6: Deploy

1. Railway will automatically deploy when you push to your repository
2. Or you can manually trigger a deployment from the **Deployments** tab
3. Watch the build logs to ensure everything installs correctly

### Step 7: Run Migrations

After the first deployment:

1. Go to your service
2. Click on the **Deployments** tab
3. Find the latest deployment
4. Click on it to view logs
5. The `release` command in Procfile should run migrations automatically

**OR** manually run migrations via Railway CLI:

```bash
railway run python manage.py migrate
```

### Step 8: Create Superuser (Optional)

To access Django admin:

```bash
railway run python manage.py createsuperuser
```

### Step 9: Verify Deployment

1. Check your service URL (Railway provides a `.railway.app` domain)
2. Test your API endpoints:
   - `https://your-app.railway.app/api/v1/articles/`
   - `https://your-app.railway.app/api/token/`
3. Check admin panel: `https://your-app.railway.app/admin/`

## Important Notes

### Static Files
- Static files are automatically collected during deployment via the `release` command
- WhiteNoise serves static files in production
- No additional configuration needed

### Media Files
- Media files uploaded by users are stored in the `media/` directory
- **Important:** Railway's filesystem is ephemeral - uploaded files will be lost on redeploy
- For production, consider using:
  - AWS S3
  - Cloudinary
  - Railway Volume (for persistent storage)

### Database
- Railway provides automatic PostgreSQL backups
- Database connection is handled automatically via environment variables

### Custom Domain (Optional)
1. Go to your service **Settings**
2. Click **"Generate Domain"** or **"Custom Domain"**
3. Add your custom domain
4. Update `ALLOWED_HOSTS` environment variable to include your custom domain

## Troubleshooting

### Build Fails
- Check build logs in Railway dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt` is compatible

### Application Crashes
- Check application logs in Railway dashboard
- Verify all environment variables are set correctly
- Ensure database is connected and migrations are run

### Static Files Not Loading
- Verify `collectstatic` ran successfully (check release logs)
- Ensure WhiteNoise middleware is in `MIDDLEWARE` list
- Check `STATIC_ROOT` and `STATIC_URL` settings

### Database Connection Issues
- Verify database environment variables are set correctly
- Check that PostgreSQL service is running
- Ensure database migrations have been run

## Railway CLI (Optional)

Install Railway CLI for easier management:

```bash
npm i -g @railway/cli
railway login
```

Then you can:
- View logs: `railway logs`
- Run commands: `railway run python manage.py migrate`
- Open shell: `railway shell`

## Support

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)

