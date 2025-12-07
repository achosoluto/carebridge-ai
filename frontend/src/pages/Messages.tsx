import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import { Send, User, Globe } from 'lucide-react';

interface Patient {
    id: number;
    name: string;
    language: string;
}

interface Message {
    id: number;
    content: string;
    translated_content: string | null;
    sender_type: 'STAFF' | 'PATIENT';
    created_at: string;
    language: string;
}

const Messages: React.FC = () => {
    const [patients, setPatients] = useState<Patient[]>([]);
    const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const [loadingMessages, setLoadingMessages] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchPatients();
    }, []);

    useEffect(() => {
        if (selectedPatient) {
            fetchMessages(selectedPatient.id);
        }
    }, [selectedPatient]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const fetchPatients = async () => {
        try {
            const response = await api.get('/patients/');
            setPatients(response.data);
        } catch (error) {
            console.error('Error fetching patients:', error);
        }
    };

    const fetchMessages = async (patientId: number) => {
        setLoadingMessages(true);
        try {
            // In a real app, filter by patientId in the query: /messages/?patient=id
            // For now, assume backend returns all or implemented filter.
            // My ViewSet implementation does not have filter backend configured explicitly yet,
            // except global standard DRF filtering if enabled.
            // I'll assume I need to implement filtering in the backend or just filter client side for prototype.
            // Ideally I should update ViewSet to allow filtering.
            const response = await api.get('/messages/');
            // Client side filter for simplicity in T10
            const filtered = response.data.filter((m: any) => m.patient === patientId);
            setMessages(filtered);
        } catch (error) {
            console.error('Error fetching messages:', error);
        } finally {
            setLoadingMessages(false);
        }
    };

    const handeSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedPatient || !newMessage.trim()) return;

        try {
            // Optimistic update? No, let's wait for server response to get translation.
            const payload = {
                patient: selectedPatient.id,
                sender_type: 'STAFF',
                content: newMessage,
                language: 'ko' // Staff writes in Korean (or EN for proto)
            };

            const response = await api.post('/messages/', payload);
            setMessages([...messages, response.data]);
            setNewMessage('');
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message');
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    return (
        <div className="flex h-[calc(100vh-8rem)] bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            {/* Patient List Sidebar */}
            <div className="w-1/3 border-r border-gray-200 overflow-y-auto">
                <div className="p-4 border-b border-gray-200 bg-gray-50">
                    <h2 className="font-semibold text-gray-700">Conversations</h2>
                </div>
                <div className="divide-y divide-gray-100">
                    {patients.map(patient => (
                        <div
                            key={patient.id}
                            onClick={() => setSelectedPatient(patient)}
                            className={`p-4 cursor-pointer hover:bg-gray-50 transition-colors ${selectedPatient?.id === patient.id ? 'bg-blue-50' : ''}`}
                        >
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-600">
                                    <User className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="font-medium text-gray-900">{patient.name}</h3>
                                    <p className="text-xs text-gray-500 flex items-center gap-1">
                                        <Globe className="w-3 h-3" />
                                        {patient.language}
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col">
                {selectedPatient ? (
                    <>
                        <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                            <h2 className="font-semibold text-gray-800">{selectedPatient.name}</h2>
                            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                                Translating to {selectedPatient.language}
                            </span>
                        </div>

                        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                            {loadingMessages ? (
                                <div className="text-center text-gray-400 mt-10">Loading messages...</div>
                            ) : messages.length === 0 ? (
                                <div className="text-center text-gray-400 mt-10">No messages yet. Start conversation.</div>
                            ) : (
                                messages.map(msg => {
                                    const isStaff = msg.sender_type === 'STAFF';
                                    return (
                                        <div key={msg.id} className={`flex ${isStaff ? 'justify-end' : 'justify-start'}`}>
                                            <div className={`max-w-[70%] rounded-2xl px-4 py-3 ${isStaff ? 'bg-primary text-white rounded-br-none' : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none'
                                                }`}>
                                                <p className="text-sm">{msg.content}</p>
                                                {msg.translated_content && (
                                                    <div className={`mt-2 pt-2 border-t text-xs opacity-90 italic ${isStaff ? 'border-blue-400' : 'border-gray-100 text-gray-500'}`}>
                                                        {msg.translated_content}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    );
                                })
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        <div className="p-4 bg-white border-t border-gray-200">
                            <form onSubmit={handeSendMessage} className="flex gap-2">
                                <input
                                    type="text"
                                    placeholder="Type a message in your language..."
                                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                    value={newMessage}
                                    onChange={e => setNewMessage(e.target.value)}
                                />
                                <button
                                    type="submit"
                                    disabled={!newMessage.trim()}
                                    className="bg-primary text-white p-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                    <Send className="w-5 h-5" />
                                </button>
                            </form>
                        </div>
                    </>
                ) : (
                    <div className="flex-1 flex flex-col items-center justify-center text-gray-400">
                        <User className="w-16 h-16 mb-4 opacity-20" />
                        <p>Select a patient to view conversation</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Messages;
