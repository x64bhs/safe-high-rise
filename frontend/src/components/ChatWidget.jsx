import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';
import chatbotIcon from '../assets/chatbot-icon.png';

// Language Map for proper TTS voice selection and Backend API
const LANGUAGES = [
    { name: "English", code: "en-US" },
    { name: "Hindi", code: "hi-IN" },
    { name: "Bengali", code: "bn-IN" },
    { name: "Telugu", code: "te-IN" },
    { name: "Tamil", code: "ta-IN" },
    { name: "Marathi", code: "mr-IN" },
    { name: "Urdu", code: "ur-IN" },
    { name: "Gujarati", code: "gu-IN" },
    { name: "Kannada", code: "kn-IN" },
    { name: "Odia", code: "or-IN" },
    { name: "Malayalam", code: "ml-IN" },
    { name: "Punjabi", code: "pa-IN" },
    { name: "Assamese", code: "as-IN" },
    { name: "Spanish", code: "es-ES" },
    { name: "French", code: "fr-FR" },
    { name: "German", code: "de-DE" },
    { name: "Mandarin", code: "zh-CN" },
    { name: "Arabic", code: "ar-SA" },
    { name: "Russian", code: "ru-RU" },
    { name: "Portuguese", code: "pt-PT" },
    { name: "Japanese", code: "ja-JP" }
];

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isMaximized, setIsMaximized] = useState(false);
    const [messages, setMessages] = useState([
        { text: "Hello! I'm StrataBot! 🏗️ How can I help you build safe and amazing high-rises today?", sender: 'bot' }
    ]);
    const [input, setInput] = useState('');
    const [selectedLang, setSelectedLang] = useState(LANGUAGES[0]);
    const [isRecording, setIsRecording] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const messagesEndRef = useRef(null);
    const recognitionRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isMaximized]);

    // Initialize Speech Recognition
    useEffect(() => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = false;
            recognitionRef.current.lang = selectedLang.code;

            recognitionRef.current.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                setInput(transcript);
                setIsRecording(false);
            };

            recognitionRef.current.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                setIsRecording(false);
            };

            recognitionRef.current.onend = () => {
                setIsRecording(false);
            };
        }
    }, [selectedLang]);

    // Load voices on mount
    useEffect(() => {
        if ('speechSynthesis' in window) {
            // Force voice loading
            const loadVoices = () => {
                const voices = window.speechSynthesis.getVoices();
                if (voices.length > 0 && !window._voicesLoaded) {
                    console.log(`Loaded ${voices.length} voices`);
                    window._voicesLoaded = true;
                }
            };
            loadVoices();
            window.speechSynthesis.onvoiceschanged = loadVoices;
        }
    }, []);

    const toggleChat = () => setIsOpen(!isOpen);
    const toggleMaximize = () => setIsMaximized(!isMaximized);

    const formatMessage = (text) => {
        const lines = text.split('\n');
        return lines.map((line, index) => {
            const trimmed = line.trim();
            if (trimmed.startsWith('*') || trimmed.startsWith('- ')) {
                const content = trimmed.substring(2);
                return <li key={index} className="chat-list-item">{parseBold(content)}</li>;
            }
            if (trimmed.length === 0) return null;
            return <p key={index} className="chat-paragraph">{parseBold(line)}</p>;
        });
    };

    const parseBold = (text) => {
        const parts = text.split(/(\*\*.*?\*\*|__.*?__)/g);
        return parts.map((part, index) => {
            if ((part.startsWith('**') && part.endsWith('**')) ||
                (part.startsWith('__') && part.endsWith('__'))) {
                return <strong key={index}>{part.slice(2, -2)}</strong>;
            }
            return part.replace(/\*/g, '');
        });
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = input;
        setMessages(prev => [...prev, { text: userMessage, sender: 'user' }]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userMessage, language: selectedLang.name }),
            });

            const data = await response.json();
            const botResponse = data.response;

            setMessages(prev => [...prev, { text: botResponse, sender: 'bot' }]);
            speak(botResponse);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { text: "Sorry, I encountered an error. Please try again.", sender: 'bot' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') handleSend();
    };

    const toggleRecording = () => {
        if (isRecording) {
            recognitionRef.current?.stop();
        } else {
            if (recognitionRef.current) {
                recognitionRef.current.lang = selectedLang.code;
                try {
                    recognitionRef.current.start();
                    setIsRecording(true);
                } catch (e) {
                    console.error("Speech start error:", e);
                }
            }
        }
    };

    const speak = (text) => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);

            // Clean text
            let cleanText = text.replace(/[\*\#\_]/g, '');
            cleanText = cleanText.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');
            cleanText = cleanText.replace(/^\s*[-•]\s+/gm, '');

            if (!cleanText.trim()) {
                console.warn("No text to speak");
                return;
            }

            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.onstart = () => setIsSpeaking(true);
            utterance.onend = () => setIsSpeaking(false);
            utterance.onerror = (e) => {
                console.error("Speech error", e);
                setIsSpeaking(false);
            }

            utterance.lang = selectedLang.code;

            const voices = window.speechSynthesis.getVoices();

            // DEBUG: Log available voices (once)
            if (!window._voicesLogged) {
                console.log("=== AVAILABLE VOICES ===");
                voices.forEach(v => console.log(`  ${v.name} (${v.lang})`));
                window._voicesLogged = true;
            }

            let matchingVoice = null;
            const shortCode = selectedLang.code.split('-')[0];

            console.log(`🔍 Voice for: ${selectedLang.name} (${selectedLang.code})`);

            // 1. Exact match + female preference
            const exactMatches = voices.filter(v => v.lang === selectedLang.code);
            if (exactMatches.length > 0) {
                console.log(`  ${exactMatches.length} exact:`, exactMatches.map(v => v.name));
                matchingVoice = exactMatches.find(v =>
                    v.name.toLowerCase().includes('female') ||
                    v.name.toLowerCase().includes('zira') ||
                    v.name.toLowerCase().includes('heera')
                );
                if (!matchingVoice) {
                    matchingVoice = exactMatches.find(v => !v.name.toLowerCase().includes('male'));
                }
                if (!matchingVoice) matchingVoice = exactMatches[0];
            }

            // 2. Prefix match
            if (!matchingVoice) {
                const prefixMatches = voices.filter(v => v.lang.startsWith(shortCode));
                if (prefixMatches.length > 0) {
                    console.log(`  ${prefixMatches.length} prefix:`, prefixMatches.map(v => `${v.name}(${v.lang})`));
                    matchingVoice = prefixMatches.find(v =>
                        v.name.toLowerCase().includes('female') ||
                        !v.name.toLowerCase().includes('male')
                    ) || prefixMatches[0];
                }
            }

            // 3. Indian language fallback to en-IN
            if (!matchingVoice && selectedLang.code.includes('-IN')) {
                console.log(`  Trying Indian English fallback...`);
                const indianEn = voices.filter(v => v.lang === 'en-IN' || (v.lang.startsWith('en') && v.name.toLowerCase().includes('india')));
                if (indianEn.length > 0) {
                    matchingVoice = indianEn.find(v => !v.name.toLowerCase().includes('male')) || indianEn[0];
                }
            }

            // 4. Any female voice
            if (!matchingVoice) {
                console.log(`  Finding any female voice...`);
                matchingVoice = voices.find(v =>
                    v.name.toLowerCase().includes('female') ||
                    v.name.toLowerCase().includes('zira')
                );
            }

            // 5. First available
            if (!matchingVoice && voices.length > 0) {
                matchingVoice = voices[0];
            }

            if (matchingVoice) {
                utterance.voice = matchingVoice;
                console.log(`✅ Using: ${matchingVoice.name}`);
            } else {
                console.warn(`⚠️ No voice found, using default`);
            }

            utterance.pitch = 1.3;
            utterance.rate = 0.95;

            console.log(`🔊 "${cleanText.substring(0, 60)}..."`);
            window.speechSynthesis.speak(utterance);
        }
    };

    const stopSpeaking = () => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);
        }
    }

    return (
        <div className={`chat-widget-container ${isOpen ? 'open' : ''}`}>
            {!isOpen && (
                <button className="chat-toggle-btn" onClick={toggleChat}>
                    <img src={chatbotIcon} alt="Chat" className="chat-icon" />
                </button>
            )}

            {isOpen && (
                <div className={`chat-window ${isMaximized ? 'maximized' : ''}`}>
                    <div className="chat-header">
                        <div className="header-title">
                            <img src={chatbotIcon} alt="StrataBot" className="header-icon" />
                            <h3>EarthBot</h3>
                        </div>
                        <div className="header-controls">
                            <button className="control-btn" onClick={toggleMaximize} title={isMaximized ? "Restore" : "Maximize"}>
                                {isMaximized ? '❐' : '□'}
                            </button>
                            <button className="control-btn close-btn" onClick={toggleChat} title="Close">✕</button>
                        </div>
                    </div>

                    <div className="chat-messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`message-wrapper ${msg.sender}`}>
                                {msg.sender === 'bot' && (
                                    <img src={chatbotIcon} alt="Bot" className="message-avatar" />
                                )}
                                <div className={`message ${msg.sender}`}>
                                    {formatMessage(msg.text)}
                                    {msg.sender === 'bot' && (
                                        <button className="speak-btn" onClick={() => speak(msg.text)} title="Read Aloud">🔊</button>
                                    )}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message bot">
                                <div className="loading-dots">
                                    <div className="dot"></div>
                                    <div className="dot"></div>
                                    <div className="dot"></div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {isSpeaking && (
                        <div className="speaking-indicator">
                            <span>Speaking...</span>
                            <button onClick={stopSpeaking} className="stop-speak-btn">Stop 🔇</button>
                        </div>
                    )}

                    <div className="chat-controls">
                        <div className="language-selector">
                            <select
                                value={selectedLang.code}
                                onChange={(e) => {
                                    const lang = LANGUAGES.find(l => l.code === e.target.value);
                                    setSelectedLang(lang || LANGUAGES[0]);
                                }}
                            >
                                {LANGUAGES.map(lang => (
                                    <option key={lang.code} value={lang.code}>
                                        {lang.name}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="input-area">
                            <input
                                type="text"
                                className="chat-input"
                                placeholder={`Ask in ${selectedLang.name}...`}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                            />
                            <button
                                className={`icon-btn ${isRecording ? 'recording' : ''}`}
                                onClick={toggleRecording}
                                title="Voice Input"
                            >
                                🎤
                            </button>
                            <button className="icon-btn" onClick={handleSend} title="Send">
                                ➤
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatWidget;
