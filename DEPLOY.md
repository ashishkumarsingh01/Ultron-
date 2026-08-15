# Ultron - Render.com Deployment

## Quick Links

- 🚀 **Deploy Guide**: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)
- 🌐 **Render.com**: https://render.com
- 📖 **API Docs**: Visit deployed app → `/docs`
- 💬 **Dashboard**: Visit deployed app → `/dashboard.html`

## 5-Minute Setup

1. **Get API Key** (2 min)
   - https://platform.openai.com/api-keys
   - Copy your key

2. **Deploy on Render** (3 min)
   - Go to https://render.com
   - Sign with GitHub
   - New → Web Service → Select Ultron-
   - Add OpenAI API key in Environment
   - Click Deploy!

3. **Access**
   - Get URL from Render
   - Visit from phone browser
   - Start chatting! 🎉

## Environment Variables

```
OPENAI_API_KEY=sk-your-key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
MEMORY_BACKEND=chroma
LOG_LEVEL=INFO
```

## Cost

- **Render**: Free tier (750 hrs/month) or $7/month
- **OpenAI**: ~$0.03 per 1K tokens

## Ready? Start at [DEPLOY_RENDER.md](DEPLOY_RENDER.md) 🚀
