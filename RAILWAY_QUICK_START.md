# Railway Quick Start - Backend Deployment

## Quick Steps

1. **Push code to GitHub/GitLab**
   ```bash
   git add .
   git commit -m "Add Railway deployment config"
   git push
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Set Root Directory**
   - Service Settings → Root Directory: `backend`

4. **Add PostgreSQL Database**
   - Click "+ New" → "Database" → "Add PostgreSQL"

5. **Set Environment Variables**
   ```
   SECRET_KEY=<generate-a-random-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=${{Postgres.DATABASE}}
   DB_USER=${{Postgres.USER}}
   DB_PASSWORD=${{Postgres.PASSWORD}}
   DB_HOST=${{Postgres.HOST}}
   DB_PORT=${{Postgres.PORT}}
   CORS_ALLOWED_ORIGINS=<your-frontend-url>
   ```

6. **Deploy**
   - Railway auto-deploys on push
   - Or manually trigger from Deployments tab

7. **Create Superuser** (optional)
   ```bash
   railway run python manage.py createsuperuser
   ```

## Your API will be available at:
`https://your-app-name.railway.app`

## Full Guide
See `RAILWAY_DEPLOYMENT.md` for detailed instructions.

