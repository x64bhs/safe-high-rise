# GitHub + Vercel Deployment Guide

This guide will walk you through pushing your project to GitHub and deploying it to Vercel.

## Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
git init
```

### 1.2 Add All Files

```bash
git add .
```

### 1.3 Create Initial Commit

```bash
git commit -m "Initial commit: Safe High-Rise application"
```

## Step 2: Push to GitHub

### 2.1 Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Click the **+** icon in the top right → **New repository**
3. Name your repository (e.g., `safe-high-rise` or `strata-mind`)
4. **Don't** initialize with README, .gitignore, or license (since you already have files)
5. Click **Create repository**

### 2.2 Connect and Push

GitHub will show you commands. Use these (replace `YOUR_USERNAME` and `YOUR_REPO_NAME`):

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**Or if you prefer SSH:**
```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy Frontend to Vercel

### 3.1 Deploy via Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login (you can use your GitHub account)
3. Click **Add New...** → **Project**
4. **Import Git Repository**: Select your GitHub repository
5. Configure the project:
   - **Framework Preset**: Vite (should auto-detect)
   - **Root Directory**: `frontend` (important!)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `dist` (default)
   - **Install Command**: `npm install` (default)
6. **Environment Variables**: Click to add:
   - Name: `VITE_API_URL`
   - Value: Your backend API URL (see Step 4 below for backend deployment options)
   - Example: `https://your-backend.railway.app` or `https://your-backend.render.com`
7. Click **Deploy**

### 3.2 Alternative: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# For production deployment
vercel --prod
```

Follow the prompts and set:
- **Root Directory**: `frontend` or `.` if you're already in frontend folder
- **Environment Variable**: `VITE_API_URL` = your backend URL

## Step 4: Deploy Backend

You have several options for the backend:

### Option A: Railway (Recommended - Easy & Free Tier)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Railway will auto-detect Python and install dependencies
6. Get your backend URL (e.g., `https://your-app.railway.app`)
7. **Update Vercel**: Go to your Vercel project → Settings → Environment Variables → Edit `VITE_API_URL` with the Railway URL

### Option B: Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **New** → **Web Service**
4. Connect your repository
5. Configure:
   - **Name**: `safe-high-rise-api`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Get your backend URL
7. Update `VITE_API_URL` in Vercel

### Option C: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set buildpack: `heroku buildpacks:set heroku/python`
5. Deploy:
   ```bash
   cd backend
   git subtree push --prefix backend heroku main
   ```
6. Get your backend URL
7. Update `VITE_API_URL` in Vercel

## Step 5: Update CORS in Backend

Make sure your backend allows requests from your Vercel domain:

In `backend/main.py`, set the `ALLOWED_ORIGINS` environment variable:

**On Railway/Render/Heroku:**
- Add environment variable: `ALLOWED_ORIGINS=https://your-frontend.vercel.app`
- Or if you have multiple: `ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com`

**For development**, you can leave it as `["*"]` or add localhost:
```python
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
```

## Step 6: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Test the application - enter coordinates and analyze a location
3. Check browser console for any errors
4. Check backend logs on Railway/Render/Heroku

## Troubleshooting

### Frontend can't connect to backend
- Verify `VITE_API_URL` is set correctly in Vercel
- Check backend CORS settings
- Ensure backend is deployed and accessible

### Build fails on Vercel
- Make sure **Root Directory** is set to `frontend`
- Check that all dependencies are in `package.json`
- Review build logs in Vercel dashboard

### Backend deployment fails
- Ensure `requirements.txt` is in the `backend` folder
- Check that **Root Directory** is set to `backend` on Railway/Render
- Verify Python version compatibility

## Repository Structure for GitHub

Your repository should look like this:
```
safe-high-rise/
├── .gitignore
├── README.md
├── DEPLOYMENT.md
├── GITHUB_VERCEL_SETUP.md
├── docker-compose.yml
├── deploy.sh
├── deploy.bat
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── Dockerfile
│   └── services/
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── vercel.json
    ├── Dockerfile
    ├── nginx.conf
    └── src/
```

## Quick Checklist

- [ ] Git repository initialized
- [ ] `.gitignore` file in place
- [ ] Code committed to Git
- [ ] Repository pushed to GitHub
- [ ] Vercel project created and connected to GitHub
- [ ] Vercel Root Directory set to `frontend`
- [ ] `VITE_API_URL` environment variable set in Vercel
- [ ] Backend deployed (Railway/Render/Heroku)
- [ ] Backend CORS configured with Vercel URL
- [ ] Application tested and working

## Next Steps

After deployment:
- Set up a custom domain in Vercel (optional)
- Enable automatic deployments on git push
- Set up monitoring/error tracking (Sentry, etc.)
- Configure SSL certificates (usually automatic)

Happy deploying! 🚀


