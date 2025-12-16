# KAALX – AI Cybersecurity Assistance Chatbot

A comprehensive web-based cybersecurity chatbot that detects phishing/scam messages, provides educational quizzes, and offers link preview analysis.

## Features

- **Phishing Detection**: Analyzes SMS, email, or links for common phishing indicators
- **Threat Classification**: Classifies messages as Safe, Suspicious, or Dangerous
- **Detailed Explanations**: Provides reasoning for the threat level
- **Cybersecurity Tips**: Offers advice on how to stay safe
- **Help Command**: Type "help" for instructions and example scam messages
- **Tools Command**: Type "tools" for a list of essential cybersecurity tools
- **Dedicated Tools Page**: Visit `/tools` for an attractive grid display of cybersecurity tools
- **Cyber Safety Quiz**: Interactive quiz at `/quiz` with random questions on cybersecurity topics
- **Link Preview Tool**: Analyze URLs at `/link-preview` for potential security risks
- **Modern Dark Theme**: Professional UI with gradients, animations, and hover effects

## Tech Stack

- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- Detection: Rule-based (no ML required)

## Installation and Running

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and go to: http://127.0.0.1:5000/

## Usage

### Chat Interface
- Enter any SMS, email text, or link in the input field
- The chatbot will analyze it and respond with threat level, explanation, and tips
- Type "help" to see instructions and example scam messages
- Type "tools" to get a list of cybersecurity tools in chat
- Type "quiz" to learn about the interactive quiz feature
- Type "preview" to learn about the link preview tool

### Tools Page (/tools)
- Dedicated page displaying cybersecurity tools in an attractive grid layout
- Navigate between chat, quiz, and link preview

### Cyber Safety Quiz (/quiz)
- Interactive quiz with 10 random cybersecurity questions
- Each question refreshes randomly for varied learning
- Immediate feedback with explanations for correct/incorrect answers
- Covers topics like HTTPS, phishing tactics, passwords, 2FA, and more

### Link Preview Tool (/link-preview)
- Analyze URLs before clicking to check for potential security risks
- Checks for HTTPS encryption, suspicious domain patterns, and security keywords
- Provides warnings and safety recommendations

## Detection Rules

The chatbot checks for:
- OTP/password requests
- Urgent scare tactics (e.g., "account blocked, verify now")
- Lottery/money gift scams
- Suspicious domains in URLs

## Project Structure

```
kaalx-chatbot/
├── app.py                 # Flask backend with detection logic, quiz, and link preview
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html         # Main chat page
│   ├── tools.html         # Tools page
│   ├── quiz.html          # Quiz page
│   └── link_preview.html  # Link preview page
├── static/
│   ├── style.css          # Modern dark theme CSS
│   └── script.js          # Frontend JavaScript
├── README.md              # This file
└── TODO.md                # Project tasks (completed)
```

The project is fully runnable and includes cybersecurity tools as requested. The app is currently running at http://127.0.0.1:5000/ with an attractive modern dark theme and dedicated tools page.
