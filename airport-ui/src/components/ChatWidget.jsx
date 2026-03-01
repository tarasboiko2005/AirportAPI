import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Bot } from 'lucide-react';
import api from '../api/axios';

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { role: 'bot', text: 'Hi! I\'m your AI flight assistant. Ask me anything about flights, airports, or bookings!' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async () => {
        const text = input.trim();
        if (!text || loading) return;

        setMessages(prev => [...prev, { role: 'user', text }]);
        setInput('');
        setLoading(true);

        try {
            const { data } = await api.post('/api/assistant/nl-query/', { prompt: text });
            const reply = typeof data.data === 'string'
                ? data.data
                : JSON.stringify(data.data, null, 2);
            setMessages(prev => [...prev, { role: 'bot', text: reply }]);
        } catch (err) {
            setMessages(prev => [...prev, {
                role: 'bot',
                text: 'Sorry, I encountered an error. Please try again.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <>
            {isOpen && (
                <div className="chat-panel">
                    <div className="chat-header">
                        <div className="chat-header-title">
                            <Bot size={18} />
                            <span>AI Assistant</span>
                        </div>
                        <button
                            className="btn btn-icon btn-secondary"
                            onClick={() => setIsOpen(false)}
                            style={{ width: 32, height: 32 }}
                        >
                            <X size={16} />
                        </button>
                    </div>
                    <div className="chat-messages">
                        {messages.map((msg, i) => (
                            <div key={i} className={`chat-message chat-message-${msg.role}`}>
                                {msg.role === 'bot' ? (
                                    <span dangerouslySetInnerHTML={{
                                        __html: msg.text.replace(/\n/g, '<br/>')
                                    }} />
                                ) : (
                                    msg.text
                                )}
                            </div>
                        ))}
                        {loading && (
                            <div className="chat-message chat-message-bot" style={{ opacity: 0.6 }}>
                                Thinking...
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="chat-input-area">
                        <input
                            className="chat-input"
                            placeholder="Ask about flights..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                        />
                        <button className="btn btn-primary btn-sm" onClick={sendMessage} disabled={loading}>
                            <Send size={16} />
                        </button>
                    </div>
                </div>
            )}
            <button className="chat-fab" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
            </button>
        </>
    );
}
