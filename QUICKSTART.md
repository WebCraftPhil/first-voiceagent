# Quick Start Guide

Get your voice agent up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- LiveKit account (free tier available)
- OpenAI API key

## Steps

### 1. Get LiveKit Credentials

1. Sign up at [livekit.io](https://livekit.io)
2. Create a new project
3. Get your credentials:
   - LiveKit URL (e.g., `wss://your-project.livekit.cloud`)
   - API Key
   - API Secret

### 2. Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an API key
3. Add credits to your account

### 3. Set Up the Project

```bash
# Clone the repository
git clone https://github.com/WebCraftPhil/first-voiceagent.git
cd first-voiceagent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 4. Configure Your Business

Edit `config.json` with your business details:

```json
{
  "business": {
    "name": "Your Business Name",
    "hours": "Monday-Friday 9:00 AM - 5:00 PM"
  },
  "faqs": [
    {
      "question": "What services do you offer?",
      "answer": "We offer..."
    }
  ]
}
```

### 5. Run the Agent

```bash
python agent.py dev
```

You should see:
```
Starting voice agent...
Voice agent running...
```

### 6. Test the Agent

#### Option A: Using LiveKit Playground

1. Go to your LiveKit project dashboard
2. Click "Test" or "Playground"
3. Join the room
4. Start speaking!

#### Option B: Using the Test Client

1. Open `test_client.html` in a browser
2. Get a room token from LiveKit dashboard
3. Enter the token and connect

### 7. View Call Summaries

After calls, check the `call_summaries/` directory for JSON files with contact info and call details.

## Common Issues

**"Module not found" error**
```bash
pip install -r requirements.txt
```

**"Connection refused" error**
- Check your LiveKit URL in `.env`
- Verify credentials are correct

**"OpenAI API error"**
- Verify your API key
- Check you have credits in your OpenAI account

## Next Steps

- Customize FAQs in `config.json`
- Add your business information
- Test with different scenarios
- Set up Twilio for phone calls (see README)

## Support

- LiveKit docs: https://docs.livekit.io
- OpenAI docs: https://platform.openai.com/docs
- Issues: https://github.com/WebCraftPhil/first-voiceagent/issues
