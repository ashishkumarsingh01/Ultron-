# Ultron - Deploy on Render.com (FREE)

## 🚀 Quick Start (5 Minutes)

### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or login
3. Create new API key
4. Copy the key

### Step 2: Create Render Account
1. Go to https://render.com
2. Click **Sign Up**
3. Choose **Sign up with GitHub**
4. Authorize Render to access your GitHub

### Step 3: Deploy Ultron
1. After login, click **New +** button (top right)
2. Select **Web Service**
3. Look for **Ultron-** repository
4. Click **Connect**
5. Fill details:
   - **Name**: `ultron-agent` (or any name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn ultron.web.server:UltronServer --host 0.0.0.0 --port $PORT`
6. Scroll down to **Environment**

### Step 4: Add API Key
1. Click **Add Environment Variable**
2. Add these:

| Key | Value |
|-----|-------|
| OPENAI_API_KEY | `sk-your-api-key-here` |
| LLM_PROVIDER | `openai` |
| LLM_MODEL | `gpt-4` |
| MEMORY_BACKEND | `chroma` |
| LOG_LEVEL | `INFO` |

3. Click **Deploy**

### Step 5: Wait for Deployment
- Takes 2-3 minutes
- You'll see a URL like: `https://ultron-agent.onrender.com`
- Open it in browser
- Done! ✅

---

## 📱 Access from Phone

Once deployed:

1. Copy your Render URL
2. On your phone, open browser
3. Visit: `https://ultron-agent.onrender.com`
4. Enjoy Ultron on your phone! 🎉

---

## 💾 Using Your Ultron

### Chat Interface
- Type messages in the chat box
- Click **Send** or press Enter
- Ultron thinks and responds

### Execute Tasks
- Describe a task (e.g., "Search for AI news and summarize")
- Click **Execute Task**
- Wait for results

### View Agent Info
- Scroll down to see:
  - Agent Name
  - LLM Model
  - Memory Backend
  - Status

---

## 🔧 Troubleshooting

### Problem: "Build Failed"
**Solution**: Check Render logs:
1. Go to your service
2. Click **Logs** tab
3. Look for error message
4. Usually it's missing API key

### Problem: "Application Error"
**Solution**:
1. Check if OpenAI API key is correct
2. Make sure key is in environment variables
3. Restart service: Click **Manual Deploy**

### Problem: "Blank Page"
**Solution**:
1. Refresh browser (Ctrl+F5)
2. Clear cache
3. Try incognito/private mode

### Problem: "API Not Responding"
**Solution**:
1. Check Render logs for errors
2. Verify OpenAI API key works
3. Wait 1-2 minutes for cold start

---

## 💰 Pricing

### Render.com
- **Free Tier**: 750 hours/month (PLENTY!)
  - Good for testing and learning
  - Apps spin down after 15 min inactivity
- **Paid**: $7/month minimum
  - Always running
  - Better for production

### OpenAI API
- **Free Trial**: $5 credit (expires in 3 months)
- **Pay as you go**: ~$0.03 per 1K tokens
- Example: 1000 queries = ~$0.30-1.00

---

## 📊 Monitor Your App

1. Go to your Render dashboard
2. Click your service
3. View:
   - **Metrics**: CPU, Memory, Bandwidth
   - **Logs**: Real-time activity
   - **Events**: Deployments, errors

---

## 🔄 Update Your App

When you update code on GitHub:

1. Push changes to GitHub
2. Render auto-deploys (if enabled)
3. Or manually deploy:
   - Go to Render dashboard
   - Click **Manual Deploy**

---

## 🛡️ Security Tips

✅ **DO**:
- Use environment variables for secrets
- Keep API keys private
- Monitor logs regularly

❌ **DON'T**:
- Share your API key
- Commit secrets to GitHub
- Use weak passwords

---

## ✨ Features Available

✅ Chat with AI (Text)
✅ Task Execution
✅ Memory Storage
✅ Web Search
✅ Real-time Updates

⚠️ Limited (requires setup):
- Voice (needs audio libraries)
- Vision (needs image libraries)
- Computer Control (only works on same machine)

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Ultron Repo**: https://github.com/ashishkumarsingh01/Ultron-
- **Issues**: GitHub Issues

---

## ✅ Deployment Checklist

- [ ] GitHub account ready
- [ ] Render account created
- [ ] OpenAI API key obtained
- [ ] Render deployment started
- [ ] Environment variables added
- [ ] App deployed successfully
- [ ] Accessed from browser
- [ ] Accessed from phone
- [ ] First chat message sent
- [ ] Enjoying Ultron! 🎉

---

**Deployed? Enjoy your AI agent! 🚀**
