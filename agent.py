"""
Voice Agent for Small Business Reception
Uses LiveKit for real-time voice interaction
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReceptionistAgent:
    """AI Voice Agent that acts as a virtual receptionist"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the receptionist agent with configuration"""
        self.config = self._load_config(config_path)
        self.call_summaries: List[Dict] = []
        self.current_call_data: Dict = {}
        
    def _load_config(self, config_path: str) -> Dict:
        """Load business configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration if config file not found"""
        return {
            "business": {
                "name": os.getenv("BUSINESS_NAME", "Small Business Solutions"),
                "hours": os.getenv("BUSINESS_HOURS", "Monday-Friday 9:00 AM - 5:00 PM")
            },
            "faqs": [],
            "lead_qualification": {"questions": []},
            "contact_fields": ["full_name", "phone_number", "email_address"]
        }
    
    def get_system_prompt(self) -> str:
        """Generate the system prompt for the AI assistant"""
        business_info = self.config.get("business", {})
        faqs = self.config.get("faqs", [])
        
        faq_text = "\n".join([
            f"Q: {faq['question']}\nA: {faq['answer']}"
            for faq in faqs
        ])
        
        prompt = f"""You are a professional virtual receptionist for {business_info.get('name', 'our business')}. 
Your role is to:
1. Greet callers warmly and professionally
2. Answer frequently asked questions about the business
3. Qualify leads by understanding their needs
4. Collect contact information for follow-up
5. Schedule consultations when appropriate
6. Provide a helpful, natural conversation experience

Business Information:
- Name: {business_info.get('name', 'Small Business Solutions')}
- Hours: {business_info.get('hours', 'Monday-Friday 9:00 AM - 5:00 PM')}
- Description: {business_info.get('description', 'A professional consulting firm')}

Frequently Asked Questions:
{faq_text}

Guidelines:
- Be conversational and natural, not robotic
- Listen carefully to the caller's needs
- Ask clarifying questions when needed
- Collect contact details (name, phone, email) before ending calls
- If you can't answer a question, let them know someone will call back
- Always be polite and professional
- Keep responses concise but complete

When collecting contact information, ask for:
- Full name
- Company name (if applicable)
- Phone number
- Email address
- Preferred contact method

Remember: You're representing the business, so maintain a professional yet friendly tone at all times.
"""
        return prompt
    
    def save_call_summary(self, summary: Dict):
        """Save call summary to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"call_summary_{timestamp}.json"
        
        try:
            # Create summaries directory if it doesn't exist
            os.makedirs("call_summaries", exist_ok=True)
            
            filepath = os.path.join("call_summaries", filename)
            with open(filepath, 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info(f"Call summary saved to {filepath}")
            self.call_summaries.append(summary)
        except Exception as e:
            logger.error(f"Error saving call summary: {e}")
    
    async def on_call_end(self, assistant: VoiceAssistant):
        """Handle call end - generate and save summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "duration": "N/A",  # Would be calculated from actual call start/end
            "contact_info": self.current_call_data.get("contact_info", {}),
            "topics_discussed": self.current_call_data.get("topics", []),
            "outcome": self.current_call_data.get("outcome", "Information provided"),
            "follow_up_required": self.current_call_data.get("follow_up", False)
        }
        
        self.save_call_summary(summary)
        self.current_call_data = {}  # Reset for next call


async def entrypoint(ctx: JobContext):
    """Main entry point for the voice agent"""
    logger.info("Starting voice agent...")
    
    # Initialize the receptionist agent
    agent = ReceptionistAgent()
    
    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    # Create participant
    participant = await ctx.wait_for_participant()
    
    logger.info(f"Participant connected: {participant.identity}")
    
    # Initialize OpenAI LLM
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=agent.get_system_prompt()
    )
    
    # Create voice assistant with OpenAI
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(voice="alloy"),
        chat_ctx=initial_ctx,
    )
    
    # Start the assistant
    assistant.start(ctx.room, participant)
    
    # Initial greeting
    await assistant.say(
        f"Hello! Thank you for calling {agent.config['business']['name']}. "
        "I'm your virtual assistant. How can I help you today?",
        allow_interruptions=True
    )
    
    # Keep the connection alive
    await asyncio.sleep(1)
    
    logger.info("Voice agent running...")


if __name__ == "__main__":
    # Run the worker
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
