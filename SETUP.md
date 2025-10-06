# Setup Guide - Universal CP Assistant

## Quick Start

### 1. Backend Setup

**Option A: Deploy on Render (Recommended)**
- Follow the complete guide in `RENDER_DEPLOYMENT.md`
- Deploy to Render.com for a permanent, free backend
- Update `extension/config.js` with your Render URL

**Option B: Run Locally**
- See "Local Development" section below

### 2. Install Chrome Extension

1. **Configure the backend URL**
   - Open `extension/config.js`
   - Replace `YOUR_RENDER_URL_HERE` with your Render backend URL
   - Example: `https://cp-assistant-backend.onrender.com`

2. **Download the extension folder** from this project
   - Download the entire `extension` folder to your local machine

3. **Load the extension in Chrome**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable **Developer mode** (toggle in top right)
   - Click **"Load unpacked"**
   - Select the `extension` folder you downloaded

4. **Verify installation**
   - You should see "CP Assistant" in your extensions list
   - The icon will appear in your Chrome toolbar

### 3. Configure Backend URL

**IMPORTANT:** Before using the extension, update the API URL:

1. Open `extension/config.js` in a text editor
2. Replace the placeholder:
```javascript
const CONFIG = {
  API_URL: 'https://your-app-name.onrender.com'  // Your Render URL here
};
```
3. Save the file

### 4. Use the Assistant

1. **Visit a supported coding platform:**
   - [LeetCode](https://leetcode.com/problems/)
   - [Codeforces](https://codeforces.com/problemset)
   - [CodeChef](https://www.codechef.com/problems/)

2. **Open a problem page**

3. **Click the floating "💬 CP Assistant" button** that appears on the page

4. **Ask questions like:**
   - "Explain this problem in simple terms"
   - "Why is my solution giving WA?"
   - "Give me hints without the full solution"
   - "Find similar problems I can practice"

## How It Works

### Multi-Agent Architecture
The system uses **LangGraph** to orchestrate three specialized AI agents:

1. **ExplainAgent** - Breaks down problems into simple terms
2. **DebugAgent** - Identifies bugs and logical errors in your code
3. **SuggestAgent** - Recommends similar problems for practice

### Intent Classification
When you ask a question, an **IntentClassifier** automatically determines which agent should handle it, ensuring you get the most relevant response.

### AI Model
Powered by **Google Gemini Flash 2.0** for fast, intelligent responses.

## Local Development (Optional)

If you want to run the backend locally instead of using Replit:

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Add your `GOOGLE_API_KEY` from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. Run: `./run.sh` (Linux/Mac) or `run.bat` (Windows)
5. Update `extension/popup/popup.js` - change `API_URL` to `http://localhost:8000`

### Or use Docker:
```bash
docker-compose up
```

## Troubleshooting

**Extension not appearing?**
- Make sure Developer mode is enabled in Chrome
- Try reloading the extension from `chrome://extensions/`

**Chat not working?**
- Check that you're on a supported platform (LeetCode, Codeforces, or CodeChef)
- Verify the backend is running (visit the API URL in your browser)

**No response from AI?**
- Make sure the Replit backend is running
- Check your internet connection
- Open browser console (F12) for error messages

## Tech Stack
- **Backend:** FastAPI, LangChain, LangGraph, Gemini Flash API
- **Frontend:** Vanilla JS, Chrome Extension APIs
- **Deployment:** Replit (live), Docker (local option)
