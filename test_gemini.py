import google.generativeai as genai
import os

# Your API key
GENAI_API_KEY = "AIzaSyAM98zNftgExLDfCtSAb8VQn20OQmHXAIs"

def test_gemini_api():
    """Test if the Gemini API key is working"""
    try:
        # Configure the API
        genai.configure(api_key=GENAI_API_KEY)
        
        # Create a model instance
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        
        # Test with a simple prompt
        test_prompt = "Hello! Can you respond in Hindi? Say 'नमस्ते, मैं आपकी कैसे मदद कर सकता हूं?'"
        
        print("Testing Gemini API...")
        print(f"API Key: {GENAI_API_KEY[:20]}...")
        print(f"Model: gemini-2.0-flash-lite")
        print(f"Test prompt: {test_prompt}")
        print("-" * 50)
        
        # Generate response
        response = model.generate_content(test_prompt)
        
        print("✅ API Test Successful!")
        print(f"Response: {response.text}")
        print("-" * 50)
        
        # Test multilingual capability
        print("Testing multilingual responses...")
        
        test_questions = [
            "What is photosynthesis?",
            "प्रकाश संश्लेषण क्या है?",
            "కాంతి సంశ్లేషణ అంటే ఏమిటి?",
            "ஒளிச்சேர்க்கை என்றால் என்ன?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\nTest {i}: {question}")
            response = model.generate_content(question)
            print(f"Response: {response.text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API Test Failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if success:
        print("\n🎉 Gemini API is working perfectly! Ready to integrate with your chatbot.")
    else:
        print("\n💥 Gemini API test failed. Please check your API key and try again.")
