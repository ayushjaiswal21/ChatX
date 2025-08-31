import os
from typing import Dict, Any

class Config:
    """Configuration class for the AI Teacher Chatbot"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.5'))
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
    
    # Chat Configuration
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '20'))
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '2000'))
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'english': 'English',
        'hindi': 'हिंदी',
        'telugu': 'తెలుగు',
        'tamil': 'தமிழ்'
    }
    
    # Educational Topics
    EDUCATIONAL_TOPICS = {
        'science': {
            'english': ['physics', 'chemistry', 'biology', 'experiment', 'theory', 'law', 'molecule', 'atom'],
            'hindi': ['विज्ञान', 'भौतिकी', 'रसायन', 'जीवविज्ञान', 'प्रयोग', 'सिद्धांत'],
            'telugu': ['విజ్ఞానం', 'భౌతిక శాస్త్రం', 'రసాయన శాస్త్రం', 'జీవ శాస్త్రం', 'ప్రయోగం'],
            'tamil': ['அறிவியல்', 'இயற்பியல்', 'வேதியியல்', 'உயிரியல்', 'சோதனை']
        },
        'mathematics': {
            'english': ['math', 'equation', 'formula', 'calculation', 'geometry', 'algebra', 'calculus'],
            'hindi': ['गणित', 'समीकरण', 'सूत्र', 'ज्यामिति', 'बीजगणित'],
            'telugu': ['గణితం', 'సమీకరణం', 'సూత్రం', 'జ్యామితి', 'బీజగణితం'],
            'tamil': ['கணிதம்', 'சமன்பாடு', 'சூத்திரம்', 'வடிவியல்', 'இயற்கணிதம்']
        },
        'history': {
            'english': ['history', 'ancient', 'civilization', 'war', 'king', 'empire', 'century'],
            'hindi': ['इतिहास', 'प्राचीन', 'सभ्यता', 'युद्ध', 'राजा', 'साम्राज्य'],
            'telugu': ['చరిత్ర', 'ప్రాచీన', 'నాగరికత', 'యుద్ధం', 'రాజు'],
            'tamil': ['வரலாறு', 'பண்டைய', 'நாகரிகம்', 'போர்', 'அரசன்']
        },
        'geography': {
            'english': ['geography', 'country', 'continent', 'ocean', 'mountain', 'river', 'climate'],
            'hindi': ['भूगोल', 'देश', 'महाद्वीप', 'समुद्र', 'पहाड़', 'नदी'],
            'telugu': ['భూగోళం', 'దేశం', 'ఖండం', 'సముద్రం', 'పర్వతం'],
            'tamil': ['புவியியல்', 'நாடு', 'கண்டம்', 'கடல்', 'மலை']
        },
        'literature': {
            'english': ['literature', 'poem', 'story', 'novel', 'author', 'writing', 'poetry'],
            'hindi': ['साहित्य', 'कविता', 'कहानी', 'उपन्यास', 'लेखक'],
            'telugu': ['సాహిత్యం', 'కవిత', 'కథ', 'నవల', 'రచయిత'],
            'tamil': ['இலக்கியம்', 'கவிதை', 'கதை', 'நாவல்', 'எழுத்தாளர்']
        }
    }
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'chatbot.log')
    
    @classmethod
    def get_topic_keywords(cls, language: str) -> Dict[str, list]:
        """Get topic keywords for a specific language"""
        keywords = {}
        for topic, lang_keywords in cls.EDUCATIONAL_TOPICS.items():
            keywords[topic] = lang_keywords.get(language, lang_keywords['english'])
        return keywords
    
    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        """Check if a language is supported"""
        return language in cls.SUPPORTED_LANGUAGES
    
    @classmethod
    def get_language_name(cls, language_code: str) -> str:
        """Get the display name for a language code"""
        return cls.SUPPORTED_LANGUAGES.get(language_code, language_code)
