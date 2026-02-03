# Deployment Steps - After GitHub

## Step 1: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Login"** → **"Login with GitHub"**
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository from the list
6. Railway will start deploying. Click on the service that was created.
7. Click **"Settings"** tab
8. Scroll down to **"Root Directory"** → Set to: `backend`
9. Scroll down to **"Deploy"** section
10. Under **"Start Command"**, enter:
    ```
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
11. Railway will automatically redeploy
12. Go back to **"Settings"** → **"Domains"** tab
13. Click **"Generate Domain"** (or use custom domain)
14. **Copy the domain URL** (e.g., `https://your-app.up.railway.app`)
15. Go back to **"Variables"** tab
16. Click **"New Variable"**
    - Name: `ALLOWED_ORIGINS`
    - Value: `https://your-frontend.vercel.app` (you'll update this after Vercel deployment)
    - Click **"Add"**

✅ **Backend is now deployed! Save the Railway URL.**

---

## Step 2: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"** → Choose **"Continue with GitHub"**
3. Authorize Vercel to access your GitHub account
4. Click **"Add New..."** button (top right)
5. Select **"Project"**
6. You'll see your repositories. Find your repository and click **"Import"**
7. **Configure Project:**
   - **Framework Preset:** Vite (should auto-detect) ✅
   - **Root Directory:** Click **"Edit"** → Change from `/` to `frontend`
   - **Build Command:** `npm run build` (auto-filled)
   - **Output Directory:** `dist` (auto-filled)
   - **Install Command:** `npm install` (auto-filled)
8. Click **"Environment Variables"** to expand it
9. Click **"Add"** button
    - **Name:** `VITE_API_URL`
    - **Value:** Paste your Railway backend URL from Step 1 (e.g., `https://your-app.up.railway.app`)
    - Click **"Save"**
10. Click **"Deploy"** button (bottom right)
11. Wait for deployment to complete (2-3 minutes)
12. **Copy your Vercel URL** (e.g., `https://your-app.vercel.app`)

✅ **Frontend is now deployed! Save the Vercel URL.**

---

## Step 3: Update Backend CORS with Vercel URL

1. Go back to **Railway** dashboard
2. Click on your backend service
3. Go to **"Variables"** tab
4. Find the `ALLOWED_ORIGINS` variable
5. Click **"Edit"** (pencil icon)
6. **Update the value** with your actual Vercel URL:
    ```
    https://your-app.vercel.app
    ```
    (Replace `your-app.vercel.app` with your actual Vercel domain)
7. Click **"Save"**
8. Railway will automatically redeploy with new CORS settings

✅ **CORS is now configured!**

---

## Step 4: Test Your Deployment

1. Open your Vercel URL in a browser (e.g., `https://your-app.vercel.app`)
2. Navigate to the Dashboard/Design page
3. Enter some coordinates (e.g., Latitude: `40.7128`, Longitude: `-74.0060` for New York)
4. Click **"Analyze"**
5. Wait for results
6. **If it works:** ✅ Success! Your app is live!
7. **If you see errors:**
    - Open browser console (F12 → Console tab)
    - Check for API connection errors
    - Verify `VITE_API_URL` in Vercel matches Railway URL
    - Verify `ALLOWED_ORIGINS` in Railway includes your Vercel URL

---

## Step 5: Update Vercel Environment Variable (if needed)

If you changed your Railway URL or want to update it:

1. Go to **Vercel** dashboard
2. Click on your project
3. Go to **"Settings"** tab
4. Click **"Environment Variables"** (left sidebar)
5. Find `VITE_API_URL`
6. Click **"Edit"** (three dots → Edit)
7. Update the value
8. Click **"Save"**
9. Go to **"Deployments"** tab
10. Click **"Redeploy"** on the latest deployment (three dots → Redeploy)

---

## Troubleshooting

### Frontend can't connect to backend
- ✅ Check Railway URL is correct in Vercel `VITE_API_URL`
- ✅ Check Railway service is running (green status)
- ✅ Check browser console for exact error

### CORS errors
- ✅ Verify `ALLOWED_ORIGINS` in Railway includes your Vercel URL
- ✅ Make sure there's no trailing slash (e.g., `https://app.vercel.app` not `https://app.vercel.app/`)

### Build fails on Vercel
- ✅ Verify Root Directory is set to `frontend` (not `/`)
- ✅ Check Vercel build logs for specific error
- ✅ Make sure `package.json` is in the `frontend` folder

### Backend deployment fails on Railway
- ✅ Verify Root Directory is set to `backend`
- ✅ Check Start Command is correct: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ Check Railway logs for Python errors

---

## Summary

✅ **Backend:** Deployed on Railway at `https://xxx.railway.app`
✅ **Frontend:** Deployed on Vercel at `https://xxx.vercel.app`
✅ **CORS:** Configured to allow Vercel domain
✅ **Environment Variables:** Set correctly on both platforms

**Your app is live! 🎉**


