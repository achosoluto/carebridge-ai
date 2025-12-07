import React, { useState } from 'react';
import api from '../services/api';

interface Message {
    text: string;
    sender: 'user' | 'bot';
}

const ChatWidget: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { text: 'Hello! How can I help you today?', sender: 'bot' }
    ]);
    const [inputValue, setInputValue] = useState('');

    const handleSendMessage = async () => {
        if (inputValue.trim()) {
            const userMessage = { text: inputValue, sender: 'user' as const };
            setMessages(prevMessages => [...prevMessages, userMessage]);
            setInputValue('');

            try {
                const response = await api.post('/api/chatbot/message/', { message: inputValue });
                const botMessage = { text: response.data.reply, sender: 'bot' as const };
                setMessages(prevMessages => [...prevMessages, botMessage]);
            } catch (error) {
                console.error('Error sending message:', error);
                const errorMessage = { text: 'Sorry, I am having trouble connecting. Please try again later.', sender: 'bot' as const };
                setMessages(prevMessages => [...prevMessages, errorMessage]);
            }
        }
    };

    return (
        <div className="fixed bottom-4 right-4 w-80 h-96 bg-white rounded-lg shadow-lg flex flex-col">
            <div className="p-4 border-b">
                <h2 className="text-lg font-semibold">Chat with us</h2>
            </div>
            <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
                {messages.map((msg, index) => (
                    <div key={index} className={`mb-4 ${msg.sender === 'user' ? 'text-right' : ''}`}>
                        <div className={`${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} p-3 rounded-lg inline-block max-w-xs`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
            </div>
            <div className="border-t p-4 bg-white">
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Type your message..."
                        className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    />
                    <button
                        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
                        onClick={handleSendMessage}
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatWidget;