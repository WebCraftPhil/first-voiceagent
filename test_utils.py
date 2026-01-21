"""
Test script for the voice agent utilities
"""
import json
from utils import CallSummaryManager, LeadQualifier, format_call_summary_email


def test_call_summary_manager():
    """Test call summary management"""
    print("Testing Call Summary Manager...")
    
    manager = CallSummaryManager(summary_dir="test_summaries")
    
    # Create a test summary
    contact_info = {
        "name": "John Doe",
        "company": "Acme Corp",
        "phone": "(555) 123-4567",
        "email": "john@acme.com",
        "preferred_contact": "email"
    }
    
    topics = [
        "Business consulting services",
        "Pricing information",
        "Scheduling consultation"
    ]
    
    summary = manager.create_summary(
        contact_info=contact_info,
        topics=topics,
        outcome="Scheduled consultation for next week",
        follow_up=True,
        notes="Interested in marketing services"
    )
    
    # Save summary
    filepath = manager.save_summary(summary)
    print(f"✓ Summary saved to: {filepath}")
    
    # Test email formatting
    email_text = format_call_summary_email(summary)
    print("\n✓ Email format:")
    print(email_text)
    
    # Retrieve summaries
    all_summaries = manager.get_all_summaries()
    print(f"\n✓ Total summaries: {len(all_summaries)}")
    
    return True


def test_lead_qualifier():
    """Test lead qualification"""
    print("\n\nTesting Lead Qualifier...")
    
    criteria = {
        "questions": [
            "What type of business do you have?",
            "What is your budget range?",
            "When do you want to start?",
            "What are your main challenges?"
        ]
    }
    
    qualifier = LeadQualifier(criteria)
    
    # Test high-quality lead
    responses = {
        "business_type": "SaaS startup",
        "budget": "$10,000-$20,000",
        "timeline": "Within 2 weeks",
        "challenges": "Need to scale marketing"
    }
    
    score = qualifier.score_lead(responses)
    print(f"\n✓ Lead Score: {score['score']}/{score['max_score']}")
    print(f"✓ Priority: {score['priority']}")
    print(f"✓ Qualified: {score['qualified']}")
    
    # Test low-quality lead
    responses_low = {
        "business_type": "Small retail shop"
    }
    
    score_low = qualifier.score_lead(responses_low)
    print(f"\n✓ Low-quality lead score: {score_low['score']}/{score_low['max_score']}")
    print(f"✓ Priority: {score_low['priority']}")
    
    return True


def test_config_loading():
    """Test configuration loading"""
    print("\n\nTesting Configuration Loading...")
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    print(f"✓ Business name: {config['business']['name']}")
    print(f"✓ Number of FAQs: {len(config['faqs'])}")
    print(f"✓ Lead qualification questions: {len(config['lead_qualification']['questions'])}")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Voice Agent Utilities Test Suite")
    print("=" * 60)
    
    try:
        test_call_summary_manager()
        test_lead_qualifier()
        test_config_loading()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
