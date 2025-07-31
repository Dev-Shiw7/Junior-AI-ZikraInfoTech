"""
Quick test without LangGraph CLI - just run your agent directly
"""
import sys
import os

# Add current directory to path so imports work
sys.path.insert(0, os.getcwd())

try:
    # Import your agent
    from main import support_agent
    
    print("✅ Successfully imported support_agent")
    print("🧪 Running test...")
    
    # Test your agent
    result = support_agent.invoke({
        "subject": "Payment issue",
        "description": "My credit card payment was declined for subscription"
    })
    
    print("\n📊 RESULTS:")
    print(f"Category: {result.get('category')}")
    print(f"Status: {'ESCALATED' if result.get('needs_review') else 'APPROVED'}")
    print(f"Attempts: {result.get('attempts', 0)}")
    
    if result.get('draft'):
        print(f"\nDraft Response:")
        print(f"{result['draft'][:200]}...")
    
    if result.get('needs_review'):
        print(f"\nEscalation Reason: {result.get('reviewer_feedback', 'N/A')}")
    
    print("\n✅ AGENT IS WORKING!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nCheck that you have:")
    print("1. main.py file in current directory")
    print("2. All src/ files in place")
    print("3. Required packages installed")
    
except Exception as e:
    print(f"❌ Runtime Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\nCurrent directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")