# 🎓 AI-Powered Teacher Chatbot

An intelligent, multilingual educational chatbot that acts as a virtual teacher, providing structured educational responses in English, Hindi, Telugu, and Tamil. Built with modern AI technologies and featuring a beautiful, responsive interface.

![AI Teacher Chatbot](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=openai)
![Multilingual](https://img.shields.io/badge/Multilingual-4%20Languages-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3+-red?style=for-the-badge&logo=flask)

## 🌟 Features

### 🤖 **AI-Powered Intelligence**
- **Google Gemini Integration**: Powered by Gemini 2.0 Flash Lite for intelligent responses
- **Fallback System**: Dummy responses when API is unavailable or rate limited
- **Context Awareness**: Understands educational topics and provides relevant explanations
- **Conversational Memory**: Maintains context throughout the chat session

### 🌍 **Multilingual Support**
- **4 Languages**: English, Hindi (हिंदी), Telugu (తెలుగు), Tamil (தமிழ்)
- **Smart Detection**: Automatically detects user's language
- **Consistent Responses**: Always responds in the same language as input
- **Cultural Context**: Provides culturally relevant examples

### 📚 **Educational Excellence**
- **Structured Responses**: Clear definitions, explanations, and examples
- **Subject Expertise**: Specialized knowledge in Science, Math, History, Geography, Literature
- **Step-by-step Learning**: Breaks down complex topics into understandable parts
- **Real-world Applications**: Connects concepts to practical examples

### 💻 **Modern Interface**
- **Dual Interface**: Web app (Flask) + Streamlit version
- **Responsive Design**: Works perfectly on desktop and mobile
- **Real-time Chat**: Smooth, instant messaging experience
- **Accessibility**: Screen reader friendly with proper ARIA labels

### ⚡ **Performance & Reliability**
- **Token Optimization**: Efficient prompt engineering to save costs
- **Error Handling**: Graceful error management and user feedback
- **Logging**: Comprehensive logging for debugging and monitoring
- **Scalable Architecture**: Easy to extend and maintain

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Google Gemini API key (optional, for full functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-teacher-chatbot.git
   cd ai-teacher-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GENAI_API_KEY=your_gemini_api_key_here" > .env
   ```

4. **Run the application**

   **Option A: Flask Web App**
   ```bash
   python app.py
   ```
   Open http://localhost:5000

   **Option B: Streamlit App**
   ```bash
   streamlit run streamlit_app.py
   ```
   Open http://localhost:8501

## 📖 Usage Guide

### Getting Started
1. **Choose your language**: Type your question in English, Hindi, Telugu, or Tamil
2. **Ask educational questions**: The chatbot specializes in academic topics
3. **Get detailed responses**: Receive structured explanations with examples
4. **Continue the conversation**: Ask follow-up questions for deeper learning

### Example Questions

**Science Questions:**
- "What is photosynthesis?" / "प्रकाश संश्लेषण क्या है?" / "కాంతి సంశ్లేషణ అంటే ఏమిటి?" / "ஒளிச்சேர்க்கை என்றால் என்ன?"

**Mathematics Questions:**
- "Explain quadratic equations" / "द्विघात समीकरण समझाएं" / "వర్గ సమీకరణాలను వివరించండి" / "இருபடிச் சமன்பாடுகளை விளக்கவும்"

**History Questions:**
- "Tell me about the Indus Valley Civilization" / "सिंधु घाटी सभ्यता के बारे में बताएं" / "సింధు లోయ నాగరికత గురించి చెప్పండి" / "சிந்து சமவெளி நாகரிகம் பற்றி சொல்லுங்கள்"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GENAI_API_KEY` | Your Google Gemini API key | None |
| `MAX_CONVERSATION_HISTORY` | Max conversation length | 20 |
| `LOG_LEVEL` | Logging level | INFO |

### Customization

The chatbot can be easily customized by modifying:
- **Topics**: Add new educational subjects in `config.py`
- **Languages**: Extend language support in the configuration
- **UI**: Customize the interface in `templates/index.html`
- **Prompts**: Modify system prompts for different teaching styles

## 🏗️ Architecture

```
ai-teacher-chatbot/
├── app.py                 # Main Flask application
├── streamlit_app.py       # Streamlit interface
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web interface
├── static/              # Static assets (CSS, JS)
└── logs/               # Application logs
```

### Key Components

1. **Language Detection**: Smart detection using Unicode ranges and keyword matching
2. **Context Analysis**: Topic detection for better educational responses
3. **Response Generation**: OpenAI API integration with fallback system
4. **Conversation Management**: History tracking and context maintenance
5. **User Interface**: Modern, responsive web interface

## 🧪 Testing

### Manual Testing
1. Test each supported language
2. Verify educational topic detection
3. Check fallback responses (without API key)
4. Test mobile responsiveness

### Automated Testing
```bash
# Run tests (when implemented)
python -m pytest tests/
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker (when implemented)
docker build -t ai-teacher-chatbot .
docker run -p 5000:5000 ai-teacher-chatbot
```

### Cloud Deployment
- **Heroku**: Easy deployment with Procfile
- **AWS**: Deploy on EC2 or Lambda
- **Google Cloud**: App Engine or Cloud Run
- **Vercel**: Serverless deployment

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google** for providing the Gemini API
- **Flask** for the web framework
- **Font Awesome** for the beautiful icons

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-teacher-chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-teacher-chatbot/discussions)
- **Email**: your.email@example.com

## 🔮 Roadmap

- [ ] Add more languages (Bengali, Marathi, Gujarati)
- [ ] Implement voice input/output
- [ ] Add image generation for explanations
- [ ] Create mobile app
- [ ] Add user authentication and progress tracking
- [ ] Implement spaced repetition learning
- [ ] Add quiz and assessment features

---

**Made with ❤️ by [Your Name]**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-teacher-chatbot?style=social)](https://github.com/yourusername/ai-teacher-chatbot)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-teacher-chatbot?style=social)](https://github.com/yourusername/ai-teacher-chatbot)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/ai-teacher-chatbot)](https://github.com/yourusername/ai-teacher-chatbot/issues)
