import { useParams } from 'react-router-dom'
import { useMessages, useCreateMessage } from '../hooks/useApi'
import { Send, ArrowLeft, Loader2, MessageSquare } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function PatientDetails() {
    const { patientId } = useParams<{ patientId: string }>()
    const navigate = useNavigate()
    const [inputValue, setInputValue] = useState('')

    const { data: messages = [], isLoading } = useMessages(parseInt(patientId || '0'))
    const createMessage = useCreateMessage()

    const handleSend = (e: React.FormEvent) => {
        e.preventDefault()
        if (!inputValue.trim() || !patientId) return

        createMessage.mutate({
            patient: parseInt(patientId),
            content: inputValue,
            direction: 'outgoing',
            channel: 'kakao',
            is_ai_handled: false,
            needs_human: false,
            patient_name: 'Staff Response',
            patient_phone: ''
        } as any)

        setInputValue('')
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
            <div className="max-w-4xl mx-auto">
                <button
                    onClick={() => navigate('/staff/messages')}
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
                >
                    <ArrowLeft className="w-5 h-5" />
                    Back to Messages
                </button>

                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200">
                    {/* Messages */}
                    <div className="h-[600px] overflow-y-auto p-6 space-y-4">
                        {isLoading ? (
                            <div className="flex justify-center items-center h-full">
                                <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
                            </div>
                        ) : messages.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-full text-gray-400">
                                <MessageSquare className="w-16 h-16 mb-4" />
                                <p>No messages yet</p>
                            </div>
                        ) : (
                            messages.map((message) => {
                                const isStaff = message.direction === 'outgoing'
                                return (
                                    <div key={message.id} className={`flex ${isStaff ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[70%] ${isStaff ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-900'} rounded-2xl px-4 py-3 shadow-sm`}>
                                            <p className="text-sm">{message.content}</p>
                                            <div className="flex items-center gap-2 mt-1">
                                                <span className="text-xs opacity-70">
                                                    {new Date(message.created_at).toLocaleTimeString()}
                                                </span>
                                                {!isStaff && message.is_ai_handled && (
                                                    <span className="text-xs opacity-70">🤖 AI</span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                )
                            })
                        )}
                    </div>

                    {/* Input */}
                    <div className="p-4 bg-gray-50 border-t border-gray-200">
                        <form onSubmit={handleSend} className="flex gap-2">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                placeholder="Type a message..."
                                className="flex-1 px-4 py-3 bg-white border border-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                                disabled={createMessage.isLoading}
                            />
                            <button
                                type="submit"
                                disabled={!inputValue.trim() || createMessage.isLoading}
                                className="p-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-lg"
                            >
                                {createMessage.isLoading ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    <Send className="w-5 h-5" />
                                )}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}
