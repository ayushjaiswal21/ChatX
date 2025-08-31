from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import random
import re
import logging
from typing import Dict, List, Optional
import json
from datetime import datetime
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Check if Gemini API key is available
GENAI_API_KEY = os.getenv('GENAI_API_KEY', 'AIzaSyAM98zNftgExLDfCtSAb8VQn20OQmHXAIs')
USE_GEMINI = bool(GENAI_API_KEY)

# Initialize Gemini only if API key is available
gemini_model = None
if USE_GEMINI:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GENAI_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite")
        logger.info("Gemini API initialized successfully")
    except ImportError:
        USE_GEMINI = False
        logger.error("google-generativeai not installed")
    except Exception as e:
        USE_GEMINI = False
        logger.error(f"Failed to initialize Gemini: {e}")

# Store conversation history in memory (in production, use a database)
conversation_history = []

# Dummy responses for different languages
DUMMY_RESPONSES = {
    'english': [
        "Great question! In simple terms, this is a fundamental concept that involves understanding the basic principles. For example, when we look at this topic, we can see how it connects to everyday life through practical applications.",
        "That's an interesting topic! Let me explain it step by step: First, we need to understand the definition. Then, we can explore some examples to make it clearer. This concept is widely used in various fields.",
        "Excellent question! This subject has three main components: theory, application, and real-world examples. Understanding these helps us grasp the bigger picture and see how everything connects together."
    ],
    'hindi': [
        "बहुत अच्छा प्रश्न! सरल शब्दों में, यह एक मौलिक अवधारणा है जिसमें बुनियादी सिद्धांतों को समझना शामिल है। उदाहरण के लिए, जब हम इस विषय को देखते हैं, तो हम देख सकते हैं कि यह व्यावहारिक अनुप्रयोगों के माध्यम से रोजमर्रा की जिंदगी से कैसे जुड़ता है।",
        "यह एक दिलचस्प विषय है! मैं इसे चरणबद्ध तरीके से समझाता हूं: पहले, हमें परिभाषा को समझना होगा। फिर, हम इसे स्पष्ट करने के लिए कुछ उदाहरण देख सकते हैं। यह अवधारणा विभिन्न क्षेत्रों में व्यापक रूप से उपयोग की जाती है।",
        "उत्कृष्ट प्रश्न! इस विषय के तीन मुख्य घटक हैं: सिद्धांत, अनुप्रयोग, और वास्तविक जीवन के उदाहरण। इन्हें समझना हमें बड़ी तस्वीर को समझने में मदद करता है।"
    ],
    'telugu': [
        "చాలా మంచి ప్రశ్న! సరళంగా చెప్పాలంటే, ఇది ప్రాథమిక సూత్రాలను అర్థం చేసుకోవడంతో కూడిన ఒక ప్రాథమిక భావన. ఉదాహరణకు, మనం ఈ విషయాన్ని చూసినప్పుడు, ఇది ఆచరణాత్మక అనువర్తనాల ద్వారా రోజువారీ జీవితంతో ఎలా అనుసంధానమవుతుందో చూడవచ్చు।",
        "ఇది ఆసక్తికరమైన విషయం! నేను దీన్ని దశలవారీగా వివరిస్తాను: మొదట, మనం నిర్వచనాన్ని అర్థం చేసుకోవాలి. తర్వాత, దీన్ని స్పష్టం చేయడానికి కొన్ని ఉదాహరణలను చూడవచ్చు. ఈ భావన వివిధ రంగాలలో విస్తృతంగా ఉపయోగించబడుతుంది।",
        "అద్భుతమైన ప్రశ్న! ఈ విషయానికి మూడు ప్రధాన భాగాలు ఉన్నాయి: సిద్ధాంతం, అనువర్తనం, మరియు వాస్తవ జీవిత ఉదాహరణలు. వీటిని అర్థం చేసుకోవడం మనకు పెద్ద చిత్రాన్ని చూడడంలో సహాయపడుతుంది।"
    ],
    'tamil': [
        "மிகச் சிறந்த கேள்வி! எளிமையான வார்த்தைகளில், இது அடிப்படைக் கொள்கைகளைப் புரிந்துகொள்வதை உள்ளடக்கிய ஒரு அடிப்படைக் கருத்து. உதாஹரணமாக, இந்த தலைப்பைப் பார்க்கும்போது, நடைமுறை பயன்பாடுகள் மூலம் இது அன்றாட வாழ்க்கையுடன் எவ்வாறு இணைகிறது என்பதைக் காணலாம்.",
        "இது ஒரு சுவாரஸ்யமான தலைப்பு! நான் இதை படிப்படியாக விளக்குகிறேன்: முதலில், நாம் வரையறையைப் புரிந்து கொள்ள வேண்டும். பின்னர், இதை தெளிவுபடுத்த சில உதாரணங்களைப் பார்க்கலாம். இந்தக் கருத்து பல்வேறு துறைகளில் பரவலாகப் பயன்படுத்தப்படுகிறது.",
        "சிறப்பான கேள்வி! இந்த விஷயத்திற்கு மூன்று முக்கிய கூறுகள் உள்ளன: கோட்பாடு, பயன்பாடு மற்றும் நிஜ வாழ்க்கை உதாரணங்கள். இவற்றைப் புரிந்துகொள்வது பெரிய படத்தைப் பார்க்க உதவுகிறது."
    ]
}

def detect_language(text: str) -> str:
    """
    Enhanced language detection with better accuracy and support for mixed text
    """
    # Remove punctuation and convert to lowercase for better detection
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Language-specific character patterns
    devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
    telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
    tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', text))
    
    # Common words in each language for better detection
    hindi_words = ['क्या', 'है', 'में', 'के', 'का', 'की', 'और', 'या', 'नहीं', 'हैं']
    telugu_words = ['ఏమిటి', 'అంటే', 'లో', 'కి', 'గా', 'మరియు', 'లేదా', 'కాదు', 'ఉన్నాయి']
    tamil_words = ['என்ன', 'ஆகும்', 'இல்', 'க்கு', 'ஆக', 'மற்றும்', 'அல்லது', 'இல்லை', 'உள்ளன']
    
    # Count language-specific words
    hindi_word_count = sum(1 for word in hindi_words if word in clean_text)
    telugu_word_count = sum(1 for word in telugu_words if word in clean_text)
    tamil_word_count = sum(1 for word in tamil_words if word in clean_text)
    
    # Determine language based on character count and word frequency
    if devanagari_chars > 0 or hindi_word_count > 0:
        return 'hindi'
    elif telugu_chars > 0 or telugu_word_count > 0:
        return 'telugu'
    elif tamil_chars > 0 or tamil_word_count > 0:
        return 'tamil'
    else:
        return 'english'

def get_educational_context(user_message: str, language: str) -> Dict[str, str]:
    """
    Extract educational context from user message for better responses
    """
    # Common educational topics and their keywords
    topics = {
        'science': ['physics', 'chemistry', 'biology', 'experiment', 'theory', 'law', 'molecule', 'atom'],
        'mathematics': ['math', 'equation', 'formula', 'calculation', 'geometry', 'algebra', 'calculus'],
        'history': ['history', 'ancient', 'civilization', 'war', 'king', 'empire', 'century'],
        'geography': ['geography', 'country', 'continent', 'ocean', 'mountain', 'river', 'climate'],
        'literature': ['literature', 'poem', 'story', 'novel', 'author', 'writing', 'poetry']
    }
    
    # Language-specific topic keywords
    hindi_topics = {
        'science': ['विज्ञान', 'भौतिकी', 'रसायन', 'जीवविज्ञान', 'प्रयोग', 'सिद्धांत'],
        'mathematics': ['गणित', 'समीकरण', 'सूत्र', 'ज्यामिति', 'बीजगणित'],
        'history': ['इतिहास', 'प्राचीन', 'सभ्यता', 'युद्ध', 'राजा', 'साम्राज्य'],
        'geography': ['भूगोल', 'देश', 'महाद्वीप', 'समुद्र', 'पहाड़', 'नदी'],
        'literature': ['साहित्य', 'कविता', 'कहानी', 'उपन्यास', 'लेखक']
    }
    
    telugu_topics = {
        'science': ['విజ్ఞానం', 'భౌతిక శాస్త్రం', 'రసాయన శాస్త్రం', 'జీవ శాస్త్రం', 'ప్రయోగం'],
        'mathematics': ['గణితం', 'సమీకరణం', 'సూత్రం', 'జ్యామితి', 'బీజగణితం'],
        'history': ['చరిత్ర', 'ప్రాచీన', 'నాగరికత', 'యుద్ధం', 'రాజు'],
        'geography': ['భూగోళం', 'దేశం', 'ఖండం', 'సముద్రం', 'పర్వతం'],
        'literature': ['సాహిత్యం', 'కవిత', 'కథ', 'నవల', 'రచయిత']
    }
    
    tamil_topics = {
        'science': ['அறிவியல்', 'இயற்பியல்', 'வேதியியல்', 'உயிரியல்', 'சோதனை'],
        'mathematics': ['கணிதம்', 'சமன்பாடு', 'சூத்திரம்', 'வடிவியல்', 'இயற்கணிதம்'],
        'history': ['வரலாறு', 'பண்டைய', 'நாகரிகம்', 'போர்', 'அரசன்'],
        'geography': ['புவியியல்', 'நாடு', 'கண்டம்', 'கடல்', 'மலை'],
        'literature': ['இலக்கியம்', 'கவிதை', 'கதை', 'நாவல்', 'எழுத்தாளர்']
    }
    
    # Select appropriate topic keywords based on language
    if language == 'hindi':
        topic_keywords = hindi_topics
    elif language == 'telugu':
        topic_keywords = telugu_topics
    elif language == 'tamil':
        topic_keywords = tamil_topics
    else:
        topic_keywords = topics
    
    # Detect topic from user message
    detected_topic = 'general'
    max_matches = 0
    
    for topic, keywords in topic_keywords.items():
        matches = sum(1 for keyword in keywords if keyword.lower() in user_message.lower())
        if matches > max_matches:
            max_matches = matches
            detected_topic = topic
    
    return {
        'topic': detected_topic,
        'language': language,
        'message_length': len(user_message)
    }

def get_dummy_response(user_message):
    """Generate dummy educational response based on detected language"""
    language = detect_language(user_message)
    responses = DUMMY_RESPONSES.get(language, DUMMY_RESPONSES['english'])
    return random.choice(responses)

def get_gemini_system_prompt(context: Dict[str, str] = None):
    """Enhanced system prompt for Gemini with educational context and better structure"""
    base_prompt = """You are an AI-powered teacher chatbot with expertise in multiple subjects. Your role is to:

1. **Language Consistency**: Always respond in the SAME language as the user's input (English/Hindi/हिंदी/Telugu/తెలుగు/Tamil/தமிழ்)

2. **Educational Structure**: Provide responses with:
   - Clear definitions and explanations
   - Relevant examples and analogies
   - Step-by-step breakdowns for complex topics
   - Real-world applications when possible

3. **Teaching Style**: 
   - Use encouraging and supportive language
   - Ask follow-up questions to deepen understanding
   - Provide multiple perspectives when relevant
   - Acknowledge when you don't know something and suggest resources

4. **Response Format**:
   - Start with a brief acknowledgment
   - Provide the main explanation
   - Include examples or analogies
   - End with a summary or follow-up question

5. **Subject-Specific Guidelines**:
   - Science: Focus on concepts, experiments, and applications
   - Mathematics: Show step-by-step solutions and explain concepts
   - History: Provide context, dates, and significance
   - Literature: Analyze themes, styles, and cultural context
   - Geography: Include maps, climate, and cultural aspects"""
    
    if context and context.get('topic') != 'general':
        topic_prompt = f"\n\nCurrent topic context: {context['topic']}. Provide detailed, subject-specific explanations."
        return base_prompt + topic_prompt
    
    return base_prompt

def generate_gemini_response(user_message: str, context: Dict[str, str]) -> str:
    """Generate response using Gemini API with rate limiting and error handling"""
    if not gemini_model:
        return get_dummy_response(user_message)
    
    try:
        # Create conversation history for context
        conversation = gemini_model.start_chat(history=[])
        
        # Add system prompt
        system_prompt = get_gemini_system_prompt(context)
        
        # Create the full prompt
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nPlease respond in {context['language']} language."
        
        # Generate response with retry logic for rate limiting
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                response = gemini_model.generate_content(full_prompt)
                return response.text
                
            except Exception as e:
                error_str = str(e).lower()
                if 'rate_limit' in error_str or 'quota' in error_str or '429' in error_str:
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limit hit, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        logger.error("Rate limit exceeded, falling back to dummy response")
                        return get_dummy_response(user_message)
                else:
                    logger.error(f"Gemini API error: {e}")
                    return get_dummy_response(user_message)
                    
    except Exception as e:
        logger.error(f"Error generating Gemini response: {e}")
        return get_dummy_response(user_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Detect language and get educational context
        detected_language = detect_language(user_message)
        context = get_educational_context(user_message, detected_language)
        
        if USE_GEMINI and gemini_model:
            # Use Gemini API
            response_text = generate_gemini_response(user_message, context)
            
            # Store in conversation history (as simple strings)
            conversation_history.append({'role': 'user', 'content': user_message})
            conversation_history.append({'role': 'assistant', 'content': response_text})
        else:
            # Use dummy responses
            response_text = get_dummy_response(user_message)
            
            # Store in conversation history (as simple strings)
            conversation_history.append({'role': 'user', 'content': user_message})
            conversation_history.append({'role': 'assistant', 'content': response_text})
        
        return jsonify({
            'response': response_text,
            'status': 'success',
            'mode': 'gemini' if USE_GEMINI else 'demo',
            'language': detected_language,
            'topic': context.get('topic', 'general')
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'success', 'message': 'Chat history cleared'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
