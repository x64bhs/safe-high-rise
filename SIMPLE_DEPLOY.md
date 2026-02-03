# Simplest Deployment Procedure

## ⚡ 3 Steps to Deploy

### 1️⃣ Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

### 2️⃣ Deploy Backend (Railway)

1. Go to **[railway.app](https://railway.app)** → Login with GitHub
2. **New Project** → **Deploy from GitHub** → Select your repo
3. Click the service → **Settings** → Set **Root Directory** = `backend`
4. **Settings** → **Domains** → **Generate Domain** → Copy the URL

✅ **Save this URL** (e.g., `https://xxx.railway.app`)

---

### 3️⃣ Deploy Frontend (Vercel)

1. Go to **[vercel.com](https://vercel.com)** → Login with GitHub
2. **Add New Project** → Import your repo
3. **Root Directory:** Change to `frontend`
4. **Environment Variables** → Add:
   - Name: `VITE_API_URL`
   - Value: Your Railway URL from step 2
5. **Deploy**

✅ **Done! Visit your Vercel URL**

---

### 🔧 Quick Fix: Update CORS

After Vercel deploys, go back to Railway:
- **Variables** → Add `ALLOWED_ORIGINS` = your Vercel URL

---

## That's it! 🎉

Your app is live at the Vercel URL.


