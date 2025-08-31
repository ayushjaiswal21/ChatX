import os
import sys
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import generate_gemini_response, detect_language, get_educational_context

def test_gemini_integration():
    """Test the Gemini integration with rate limiting handling"""
    
    test_cases = [
        {
            'message': 'What is photosynthesis?',
            'expected_language': 'english',
            'expected_topic': 'science'
        },
        {
            'message': 'प्रकाश संश्लेषण क्या है?',
            'expected_language': 'hindi',
            'expected_topic': 'science'
        },
        {
            'message': 'కాంతి సంశ్లేషణ అంటే ఏమిటి?',
            'expected_language': 'telugu',
            'expected_topic': 'science'
        }
    ]
    
    print("🧪 Testing Gemini Integration...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['message']}")
        
        # Test language detection
        detected_lang = detect_language(test_case['message'])
        print(f"   Language Detection: {detected_lang} (expected: {test_case['expected_language']})")
        
        # Test context analysis
        context = get_educational_context(test_case['message'], detected_lang)
        print(f"   Topic Detection: {context['topic']} (expected: {test_case['expected_topic']})")
        
        # Test Gemini response generation
        print("   Generating Gemini response...")
        try:
            response = generate_gemini_response(test_case['message'], context)
            print(f"   ✅ Response received: {response[:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Add delay to avoid rate limiting
        if i < len(test_cases):
            print("   ⏳ Waiting 3 seconds to avoid rate limiting...")
            time.sleep(3)
    
    print("\n" + "=" * 50)
    print("🎉 Integration test completed!")

if __name__ == "__main__":
    test_gemini_integration()
