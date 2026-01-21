# Voice Agent Receptionist

A real-time AI voice agent that acts as a virtual receptionist for small businesses. Built with LiveKit and OpenAI, it answers calls when staff are unavailable, speaks naturally with callers, and guides them through intake and scheduling flows.

## Features

- 🎙️ **Real-time Voice Interaction**: Natural conversation using LiveKit's voice infrastructure
- 🤖 **AI-Powered Responses**: Uses OpenAI GPT-4 for intelligent, context-aware conversations
- 📋 **FAQ Answering**: Automatically answers common business questions
- 🎯 **Lead Qualification**: Collects and qualifies leads through conversational flow
- 📞 **Contact Collection**: Gathers caller information for follow-up
- 📊 **Call Summaries**: Generates structured summaries of each call
- ☎️ **Phone Integration Ready**: Prepared for Twilio integration (coming soon)

## How It Works

1. **Caller connects** to the LiveKit room via phone (through Twilio integration) or web interface
2. **AI agent greets** the caller and asks how it can help
3. **Natural conversation** happens - the agent can:
   - Answer frequently asked questions
   - Qualify leads by understanding their needs
   - Collect contact information
   - Schedule consultations
   - Provide business information
4. **Call summary** is automatically generated and saved when the call ends

## Setup

### Prerequisites

- Python 3.8 or higher
- LiveKit account ([sign up here](https://livekit.io))
- OpenAI API key ([get one here](https://platform.openai.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WebCraftPhil/first-voiceagent.git
   cd first-voiceagent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   OPENAI_API_KEY=your-openai-api-key
   BUSINESS_NAME=Your Business Name
   BUSINESS_HOURS=Monday-Friday 9:00 AM - 5:00 PM EST
   ```

4. **Customize business configuration**
   
   Edit `config.json` to add your:
   - Business information
   - FAQs
   - Lead qualification questions
   - Contact fields to collect

### Running the Agent

Start the voice agent worker:

```bash
python agent.py dev
```

The agent will connect to LiveKit and wait for incoming calls.

### Testing

You can test the agent using:
- LiveKit's web interface
- A custom web app that connects to your LiveKit room
- Phone calls (after Twilio integration is set up)

## Configuration

### config.json

The `config.json` file controls the agent's behavior:

```json
{
  "business": {
    "name": "Your Business Name",
    "description": "What your business does",
    "hours": "Business hours",
    "phone": "Contact phone",
    "email": "Contact email"
  },
  "faqs": [
    {
      "question": "What are your hours?",
      "answer": "We're open Monday-Friday 9-5 PM"
    }
  ],
  "lead_qualification": {
    "questions": [
      "What type of business do you have?",
      "What challenges are you facing?"
    ]
  }
}
```

## Call Summaries

Call summaries are automatically saved to `call_summaries/` directory as JSON files.

Each summary includes:
- Timestamp and date
- Contact information (name, company, phone, email)
- Topics discussed
- Call outcome
- Follow-up requirements
- Additional notes

### Exporting Contacts

You can export all collected contacts to CSV:

```python
from utils import CallSummaryManager

manager = CallSummaryManager()
manager.export_contacts_csv("contacts.csv")
```

## Twilio Integration (Coming Soon)

Phone connectivity via Twilio is planned. See `twilio_integration.py` for setup instructions.

The integration will allow:
- Real phone calls to reach the AI agent
- SIP connectivity between Twilio and LiveKit
- Webhook handling for call routing
- Call recording and transcription

## Project Structure

```
first-voiceagent/
├── agent.py                 # Main voice agent implementation
├── utils.py                 # Call summaries and lead qualification
├── twilio_integration.py    # Twilio setup (placeholder)
├── config.json             # Business configuration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── call_summaries/        # Saved call summaries (created at runtime)
```

## Development

### Adding New FAQs

Edit `config.json` and add to the `faqs` array:

```json
{
  "question": "Your question here?",
  "answer": "The answer to provide"
}
```

### Customizing the Agent Behavior

Edit the system prompt in `agent.py`:

```python
def get_system_prompt(self) -> str:
    # Customize the prompt to change agent behavior
    ...
```

### Handling Special Cases

You can extend the `ReceptionistAgent` class to add custom logic for specific scenarios.

## Security Notes

- Never commit your `.env` file
- Keep your API keys secure
- Use environment variables for sensitive data
- Review call summaries for PII compliance
- Consider GDPR/privacy requirements for your region

## Troubleshooting

**Agent not connecting:**
- Verify LiveKit credentials in `.env`
- Check LiveKit server is running
- Ensure network connectivity

**OpenAI errors:**
- Verify API key is valid
- Check OpenAI account has credits
- Review rate limits

**No audio:**
- Check LiveKit audio settings
- Verify microphone permissions
- Test with LiveKit Playground first

## Future Enhancements

- [ ] Full Twilio phone integration
- [ ] Calendar integration for scheduling
- [ ] CRM integration
- [ ] Multi-language support
- [ ] Custom voice options
- [ ] Analytics dashboard
- [ ] SMS follow-up
- [ ] Email notifications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check LiveKit documentation: https://docs.livekit.io
- OpenAI documentation: https://platform.openai.com/docs

## Acknowledgments

- Built with [LiveKit](https://livekit.io) - Real-time communication platform
- Powered by [OpenAI](https://openai.com) - AI capabilities
- Inspired by the need for accessible virtual reception solutions
