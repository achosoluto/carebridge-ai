import { useState } from 'react'
import { useMessages, useCreateMessage } from '../hooks/useApi'
import { Send, MessageSquare, Loader2 } from 'lucide-react'

export default function PatientMessages() {
    const [inputValue, setInputValue] = useState('')
    const [language, setLanguage] = useState<'ko' | 'en' | 'zh' | 'ja'>('ko')

    const patientId = 1 // Mock patient ID - in real app this would come from auth
    const { data: messages = [], isLoading } = useMessages(patientId)
    const createMessage = useCreateMessage()

    const handleSend = (e: React.FormEvent) => {
        e.preventDefault()
        if (!inputValue.trim() || createMessage.isLoading) return

        createMessage.mutate({
            patient: patientId,
            content: inputValue,
            direction: 'incoming',
            channel: 'kakao',
            is_ai_handled: true,
            needs_human: false,
            patient_name: 'Demo Patient',
            patient_phone: '+821012345678'
        } as any)

        setInputValue('')
    }

    const languages = [
        { code: 'ko', label: '한국어', flag: '🇰🇷' },
        { code: 'en', label: 'English', flag: '🇺🇸' },
        { code: 'zh', label: '中文', flag: '🇨🇳' },
        { code: 'ja', label: '日本語', flag: '🇯🇵' },
    ]

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex flex-col">
            {/* Header */}
            <header className="bg-white shadow-sm px-4 py-3 border-b border-gray-200">
                <div className="max-w-3xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg">
                            CB
                        </div>
                        <h1 className="font-semibold text-gray-900 text-lg">CareBridge AI</h1>
                    </div>

                    <div className="flex items-center gap-2">
                        <select
                            value={language}
                            onChange={(e) => setLanguage(e.target.value as any)}
                            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            {languages.map((lang) => (
                                <option key={lang.code} value={lang.code}>
                                    {lang.flag} {lang.label}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            </header>

            {/* Messages Area */}
            <main className="flex-1 max-w-3xl mx-auto w-full p-4">
                <div className="bg-white rounded-2xl shadow-xl h-[calc(100vh-200px)] flex flex-col overflow-hidden border border-gray-200">
                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {isLoading ? (
                            <div className="flex justify-center items-center h-full">
                                <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
                            </div>
                        ) : messages.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-full text-gray-400">
                                <MessageSquare className="w-16 h-16 mb-4" />
                                <p>No messages yet. Start a conversation!</p>
                            </div>
                        ) : (
                            messages.map((message) => {
                                const isPatient = message.direction === 'incoming'
                                return (
                                    <div key={message.id} className={`flex ${isPatient ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[70%] ${isPatient ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-900'} rounded-2xl px-4 py-3 shadow-sm`}>
                                            <p className="text-sm">{message.content}</p>
                                            <div className="flex items-center gap-2 mt-1">
                                                <span className="text-xs opacity-70">
                                                    {new Date(message.created_at).toLocaleTimeString()}
                                                </span>
                                                {!isPatient && message.is_ai_handled && (
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
                                placeholder={language === 'ko' ? '메시지를 입력하세요...' : 'Type a message...'}
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
            </main>
        </div>
    )
}
