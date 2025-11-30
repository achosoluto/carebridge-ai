import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, AlertCircle } from 'lucide-react'
import { Message } from '../types'
import { formatRelativeTime, getConfidenceColor } from '../utils/helpers'

interface ChatInterfaceProps {
    messages: Message[]
    onSendMessage: (content: string) => void
    isLoading?: boolean
    userType: 'patient' | 'staff'
    placeholder?: string
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
    messages,
    onSendMessage,
    isLoading = false,
    userType,
    placeholder = 'Type a message...'
}) => {
    const [inputValue, setInputValue] = useState('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (inputValue.trim() && !isLoading) {
            onSendMessage(inputValue)
            setInputValue('')
        }
    }

    const isOwnMessage = (message: Message) => {
        if (userType === 'patient') {
            return message.direction === 'incoming' // Patient sent it
        }
        return message.direction === 'outgoing' // Staff sent it
    }

    return (
        <div className="flex flex-col h-full bg-gray-50 rounded-xl overflow-hidden border border-gray-200 shadow-sm">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => {
                    const isOwn = isOwnMessage(message)

                    return (
                        <div
                            key={message.id}
                            className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`flex max-w-[80%] ${isOwn ? 'flex-row-reverse' : 'flex-row'} items-end gap-2`}>
                                {/* Avatar */}
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isOwn ? 'bg-healthcare-primary text-white' : 'bg-gray-200 text-gray-600'
                                    }`}>
                                    {isOwn ? <User size={16} /> : (message.is_ai_handled ? <Bot size={16} /> : <User size={16} />)}
                                </div>

                                {/* Message Bubble */}
                                <div className={`flex flex-col ${isOwn ? 'items-end' : 'items-start'}`}>
                                    <div
                                        className={`px-4 py-2 rounded-2xl text-sm ${isOwn
                                                ? 'bg-healthcare-primary text-white rounded-br-none'
                                                : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
                                            }`}
                                    >
                                        {message.content}
                                    </div>

                                    {/* Metadata */}
                                    <div className="flex items-center gap-2 mt-1 text-xs text-gray-500">
                                        <span>{formatRelativeTime(message.created_at)}</span>
                                        {!isOwn && message.is_ai_handled && (
                                            <span className={`flex items-center gap-1 ${getConfidenceColor(message.confidence_score)}`}>
                                                <Bot size={10} />
                                                AI
                                            </span>
                                        )}
                                        {!isOwn && message.needs_human && (
                                            <span className="flex items-center gap-1 text-red-600">
                                                <AlertCircle size={10} />
                                                Human Needed
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                })}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t border-gray-200">
                <form onSubmit={handleSubmit} className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder={placeholder}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-healthcare-primary focus:border-transparent transition-all"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!inputValue.trim() || isLoading}
                        className={`p-2 rounded-full text-white transition-colors ${!inputValue.trim() || isLoading
                                ? 'bg-gray-300 cursor-not-allowed'
                                : 'bg-healthcare-primary hover:bg-healthcare-secondary'
                            }`}
                    >
                        {isLoading ? <Loader2 size={20} className="animate-spin" /> : <Send size={20} />}
                    </button>
                </form>
            </div>
        </div>
    )
}

export default ChatInterface
