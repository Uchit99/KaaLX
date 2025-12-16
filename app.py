from flask import Flask, request, jsonify, render_template, session
import re
from urllib.parse import urlparse
import random
import os 

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "kaalx_secret_key") # For session management

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# Quiz questions
quiz_questions = [
    {
        "question": "What does 'HTTPS' stand for?",
        "options": ["HyperText Transfer Protocol Secure", "HyperText Transfer Protocol Standard", "High Transfer Protocol Secure", "Hyper Transfer Text Protocol"],
        "correct": 0,
        "explanation": "HTTPS stands for HyperText Transfer Protocol Secure, which encrypts data between your browser and the website."
    },
    {
        "question": "Which of these is a common phishing tactic?",
        "options": ["Creating urgency with 'Your account will be suspended'", "Offering free antivirus software", "Asking for your favorite color", "Sending birthday greetings"],
        "correct": 0,
        "explanation": "Scammers create urgency to make you act quickly without thinking, like claiming your account will be suspended."
    },
    {
        "question": "What should you do if you receive an email asking for your password?",
        "options": ["Reply with your password", "Click the link and enter your details", "Contact the company directly through official channels", "Ignore it and delete"],
        "correct": 2,
        "explanation": "Legitimate companies never ask for passwords via email. Always contact them through official websites or phone numbers."
    },
    {
        "question": "What is a strong password?",
        "options": ["password123", "YourName1990", "P@ssw0rd!2024#Secure", "123456"],
        "correct": 2,
        "explanation": "Strong passwords include uppercase, lowercase, numbers, and special characters, and are at least 12 characters long."
    },
    {
        "question": "What does 'two-factor authentication' (2FA) do?",
        "options": ["Makes your password twice as long", "Requires two passwords", "Adds an extra layer of security beyond your password", "Allows two people to access your account"],
        "correct": 2,
        "explanation": "2FA requires a second form of verification, like a code sent to your phone, making it harder for hackers to access your account."
    },
    {
        "question": "Which of these URLs looks suspicious?",
        "options": ["https://www.paypal.com/login", "https://paypal-secure-login.com", "https://www.paypal.com/verify", "https://paypal.com/update-info"],
        "correct": 1,
        "explanation": "Suspicious URLs often use slight variations of legitimate domains, like adding words or using different TLDs."
    },
    {
        "question": "What should you do with suspicious attachments in emails?",
        "options": ["Open them immediately", "Save them for later", "Delete without opening or scan with antivirus first", "Forward to friends"],
        "correct": 2,
        "explanation": "Never open suspicious attachments. They may contain malware. Delete them or scan with antivirus software."
    },
    {
        "question": "What is social engineering in cybersecurity?",
        "options": ["Building social networks", "Manipulating people to reveal confidential information", "Engineering social media algorithms", "Creating social apps"],
        "correct": 1,
        "explanation": "Social engineering involves psychological manipulation to trick people into giving away sensitive information or performing actions."
    },
    {
        "question": "Why should you keep your software updated?",
        "options": ["To get new features", "To fix security vulnerabilities", "To make your computer slower", "To increase file sizes"],
        "correct": 1,
        "explanation": "Software updates often include security patches that fix known vulnerabilities that hackers could exploit."
    },
    {
        "question": "What is phishing?",
        "options": ["Fishing with a computer", "A type of malware", "Fraudulent attempt to obtain sensitive information", "A way to catch fish online"],
        "correct": 2,
        "explanation": "Phishing is a cyber attack where scammers try to trick you into revealing personal information through fake emails, websites, or messages."
    },
    {
        "question": "What is the difference between white-hat and black-hat hackers?",
        "options": ["White-hat hackers are ethical and help improve security, black-hat hackers exploit vulnerabilities for personal gain", "White-hat hackers wear white hats, black-hat hackers wear black hats", "White-hat hackers work for governments, black-hat hackers work for companies", "There is no difference"],
        "correct": 0,
        "explanation": "White-hat hackers (ethical hackers) identify and fix security flaws with permission, while black-hat hackers exploit them illegally."
    },
    {
        "question": "What is SQL injection?",
        "options": ["A type of database query", "An attack where malicious SQL code is inserted into a query to manipulate a database", "A way to inject vaccines", "A SQL programming language"],
        "correct": 1,
        "explanation": "SQL injection is a code injection technique that exploits vulnerabilities in an application's software by inserting malicious SQL statements."
    },
    {
        "question": "What does XSS stand for in cybersecurity?",
        "options": ["Extra Secure System", "Cross-Site Scripting", "Xtreme Security Software", "XML Secure Script"],
        "correct": 1,
        "explanation": "XSS (Cross-Site Scripting) is a vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users."
    },
    {
        "question": "What is a DDoS attack?",
        "options": ["A denial-of-service attack using multiple compromised systems", "A type of encryption", "A way to download files faster", "A database query"],
        "correct": 0,
        "explanation": "DDoS (Distributed Denial of Service) overwhelms a target with traffic from multiple sources, making it unavailable."
    },
    {
        "question": "What is social engineering?",
        "options": ["Building social networks", "Manipulating people to divulge confidential information", "Engineering social media", "Creating social apps"],
        "correct": 1,
        "explanation": "Social engineering exploits human psychology to gain access to systems or information, often through deception."
    },
    {
        "question": "What is a zero-day vulnerability?",
        "options": ["A vulnerability known for zero days", "A flaw unknown to the vendor and without a patch", "A bug that crashes systems immediately", "A type of antivirus"],
        "correct": 1,
        "explanation": "A zero-day is a software vulnerability unknown to the vendor, giving attackers a window to exploit it before a fix is available."
    },
    {
        "question": "What is encryption?",
        "options": ["Compressing files", "Converting data into a coded format to prevent unauthorized access", "Deleting data permanently", "Backing up data"],
        "correct": 1,
        "explanation": "Encryption transforms readable data into an unreadable format using algorithms, requiring a key to decrypt it."
    },
    {
        "question": "What is a firewall?",
        "options": ["A physical wall in a building", "A network security system that monitors and controls incoming and outgoing traffic", "A type of antivirus", "A backup device"],
        "correct": 1,
        "explanation": "A firewall acts as a barrier between a trusted network and untrusted networks, blocking unauthorized access."
    },
    {
        "question": "What is malware?",
        "options": ["Software for managing emails", "Malicious software designed to harm or exploit devices", "A type of hardware", "A web browser"],
        "correct": 1,
        "explanation": "Malware includes viruses, worms, trojans, and ransomware that can steal data, damage systems, or disrupt operations."
    }
]

def detect_phishing(message):
    message_lower = message.lower()
    threat_level = "Safe"
    explanation = "This message appears to be safe."
    tips = ["Always verify the sender's identity.", "Do not click on suspicious links."]

    flags = []

    if re.search(r'\b(otp|password|verify|code|pin|login|signin)\b', message_lower):
        flags.append("OTP/Password Request")
        threat_level = "Suspicious"
        explanation = "This message requests sensitive information like OTP or password, which could be a phishing attempt."
        tips.append("Never share OTPs or passwords via SMS/email.")

    if not flags:
        explanation = "No red flags detected in this message."
        tips = ["Stay vigilant against phishing attempts.", "Use antivirus software."]

    return {
        "threat_level": threat_level,
        "explanation": explanation,
        "tips": tips
    }

@app.route('/tools')
def tools():
    tools_list = [
        "VirusTotal: Online virus scanner for files and URLs",
        "Have I Been Pwned: Check if your email has been compromised",
        "Malwarebytes: Anti-malware software",
        "LastPass: Password manager",
        "uBlock Origin: Browser extension for ad blocking",
        "Wireshark: Network protocol analyzer",
        "Nmap: Network discovery and security auditing tool",
        "Metasploit: Penetration testing framework",
        "Burp Suite: Web vulnerability scanner",
        "John the Ripper: Password cracking tool",
        "Aircrack-ng: Wireless network security suite",
        "Snort: Intrusion detection system",
        "OSSEC: Host-based intrusion detection",
        "OpenVAS: Vulnerability scanner",
        "Nikto: Web server scanner",
        "SQLMap: SQL injection tool",
        "OWASP ZAP: Web application security scanner",
        "Kali Linux: Penetration testing distribution",
        "Hashcat: Advanced password recovery tool",
        "Hydra: Online password cracking tool",
        "Nessus: Vulnerability assessment scanner",
        "tcpdump: Command-line packet analyzer",
        "Ettercap: Man-in-the-middle attack tool",
        "BeEF: Browser exploitation framework",
        "SET (Social-Engineer Toolkit): Social engineering tools",
        "Recon-ng: Web reconnaissance framework",
        "Dirbuster: Web content scanner",
        "Exploit-DB: Database of exploits"
    ]
    return render_template('tools.html', tools=tools_list)

@app.route('/quiz')
def quiz():
    question_index = random.randint(0, len(quiz_questions) - 1)
    question = quiz_questions[question_index]
    return render_template('quiz.html', question=question, question_index=question_index)

@app.route('/api/quiz-answer', methods=['POST'])
def quiz_answer():
    data = request.get_json()
    question_index = data.get('question_index', 0)
    selected_answer = data.get('answer', -1)

    question = quiz_questions[question_index]
    is_correct = selected_answer == question['correct']

    return jsonify({
        'correct': is_correct,
        'explanation': question['explanation'],
        'correct_answer': question['options'][question['correct']]
    })

@app.route('/link-preview')
def link_preview():
    return render_template('link_preview.html')

@app.route('/api/preview-link', methods=['POST'])
def preview_link():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'No URL provided'})

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed = urlparse(url)

    return jsonify({
        'url': url,
        'domain': parsed.netloc,
        'warnings': [],
        'safe': True
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    return jsonify(detect_phishing(user_message))

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
