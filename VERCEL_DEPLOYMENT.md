# Vercel Deployment Guide

## 📋 Prerequisites

1. GitHub account
2. Vercel account (sign up at https://vercel.com)
3. Project already cleaned and ready to push

## 🚀 Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git (if not already initialized)
git init

# Add all files (respecting .gitignore)
git add .

# Commit changes
git commit -m "Initial commit for Vercel deployment"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Connect Vercel to GitHub

1. Login to Vercel: https://vercel.com/login
2. Click "Add New" → "Project"
3. Select your GitHub repository
4. Vercel will detect Next.js projects automatically

### 3. Configure Frontend Apps

#### Admin App (Port 3001 - Admin Dashboard)

**Project Settings:**
- Framework Preset: `Next.js`
- Root Directory: `Frontend/admin-app`
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)

**Environment Variables:**
```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

#### User App (Port 3000 - Public Interface)

**Project Settings:**
- Framework Preset: `Next.js`
- Root Directory: `Frontend/nextjs-app`
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)

**Environment Variables:**
```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

### 4. Deploy

1. Click "Deploy" - Vercel will automatically:
   - Install dependencies (`npm install`)
   - Run build (`npm run build`)
   - Deploy to production

2. Wait for deployment (usually 2-5 minutes)

3. Get deployment URLs:
   - Admin App: `https://admin-app-xxx.vercel.app`
   - User App: `https://nextjs-app-xxx.vercel.app`

## 🔧 Important Notes

### What Gets Deployed to Vercel?
- ✅ Frontend/admin-app (Admin Dashboard)
- ✅ Frontend/nextjs-app (Public User Interface)
- ❌ Backend (FastAPI) - Deploy separately
- ❌ Model IndoBERT - Stays in HuggingFace Space

### Backend Deployment
Backend FastAPI harus di-deploy terpisah ke:
- Railway (https://railway.app)
- Render (https://render.com)
- DigitalOcean
- AWS EC2
- Azure App Service

### Model Inference
- Model tetap di HuggingFace Space
- Backend akan call HF Space API untuk inference
- Retrain tetap dilakukan di local (laptop dengan GPU)

## 🔐 Environment Variables Setup

### Admin App (.env.local)
```bash
# Production API URL
NEXT_PUBLIC_API_URL=https://your-backend-api.com

# Optional: Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### User App (.env.local)
```bash
# Production API URL
NEXT_PUBLIC_API_URL=https://your-backend-api.com

# Optional: Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### Backend (.env) - Deploy separately
```bash
# Hugging Face
HF_TOKEN=hf_xxxxxxxxxxxxx
HF_SPACE_NAME=username/space-name

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# CORS Origins (add Vercel URLs)
CORS_ORIGINS=["https://admin-app-xxx.vercel.app","https://nextjs-app-xxx.vercel.app"]
```

## ⚙️ Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain (e.g., `admin.yourdomain.com`)
3. Configure DNS records as instructed
4. Wait for SSL certificate (automatic)

## 🐛 Troubleshooting

### Build Fails
- Check build logs in Vercel dashboard
- Verify all dependencies in `package.json`
- Ensure no TypeScript errors locally (`npm run build`)

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is deployed and accessible

### Environment Variables Not Working
- Environment variables must start with `NEXT_PUBLIC_` to be accessible in browser
- Redeploy after adding/changing environment variables

## 📊 Monitoring

Vercel provides:
- Real-time logs
- Analytics (page views, performance)
- Web Vitals monitoring
- Error tracking

Access via: https://vercel.com/dashboard

## 🔄 Continuous Deployment

After initial setup, every push to `main` branch will:
1. Trigger automatic deployment
2. Run build process
3. Deploy to production
4. Update live URLs

## 📝 Architecture Flow

```
┌─────────────────────────────────────────────────┐
│                    Users                        │
└────────────┬──────────────────┬─────────────────┘
             │                  │
             v                  v
    ┌────────────────┐  ┌────────────────┐
    │  Admin App     │  │  Public App    │
    │  (Vercel)      │  │  (Vercel)      │
    │  Port 3001     │  │  Port 3000     │
    └────────┬───────┘  └────────┬───────┘
             │                   │
             └────────┬──────────┘
                      v
             ┌────────────────┐
             │  Backend API   │
             │  (Railway/     │
             │   Render/etc)  │
             └────────┬───────┘
                      v
             ┌────────────────┐
             │  HF Space      │
             │  (Inference)   │
             └────────────────┘
```

## ✅ Deployment Checklist

- [ ] .gitignore updated (models, node_modules, .env)
- [ ] Cleanup completed (.next, __pycache__, .venv)
- [ ] .env.example files created
- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] Admin app deployed
- [ ] User app deployed
- [ ] Backend deployed separately
- [ ] CORS origins updated in backend
- [ ] Test all API connections
- [ ] Monitor for errors

## 🎉 Post-Deployment

1. Test admin dashboard: Login, check stats, model management
2. Test public app: News detection, hasil detection
3. Monitor Vercel analytics
4. Set up custom domain (optional)
5. Configure CI/CD workflows (optional)

---

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/docs/deployment
- Support: https://vercel.com/support
