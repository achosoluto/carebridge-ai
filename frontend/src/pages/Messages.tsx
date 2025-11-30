import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { usePatients, useMessages } from '../hooks/useApi'
import { MessageSquare, Search, Filter, User, Clock, Bot, AlertCircle, ChevronRight } from 'lucide-react'

export default function Messages() {
    const navigate = useNavigate()
    const [searchTerm, setSearchTerm] = useState('')
    const [filterStatus, setFilterStatus] = useState<'all' | 'needs-human' | 'ai-handled'>('all')

    const { data: patients = [], isLoading: patientsLoading } = usePatients()
    const { data: messages = [], isLoading: messagesLoading } = useMessages()

    // Group messages by patient
    const patientConversations = patients.map(patient => {
        const patientMessages = messages.filter(m => m.patient === patient.id)
        const lastMessage = patientMessages[0] // Assuming messages are sorted by date desc

        return {
            patient,
            messages: patientMessages,
            lastMessage,
            unreadCount: patientMessages.filter(m => m.needs_human).length
        }
    }).filter(conv => conv.messages.length > 0)

    // Apply filters
    const filteredConversations = patientConversations.filter(conv => {
        const matchesSearch = conv.patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            conv.patient.phone.includes(searchTerm)

        let matchesFilter = true
        if (filterStatus === 'needs-human') {
            matchesFilter = conv.messages.some(m => m.needs_human)
        } else if (filterStatus === 'ai-handled') {
            matchesFilter = conv.messages.every(m => m.is_ai_handled && !m.needs_human)
        }

        return matchesSearch && matchesFilter
    })

    const isLoading = patientsLoading || messagesLoading

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2">Patient Messages</h1>
                    <p className="text-gray-600">View and manage all patient conversations</p>
                </div>

                {/* Filters */}
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search by patient name or phone..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div className="relative">
                            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <select
                                value={filterStatus}
                                onChange={(e) => setFilterStatus(e.target.value as any)}
                                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none"
                            >
                                <option value="all">All Conversations</option>
                                <option value="needs-human">Needs Human Attention</option>
                                <option value="ai-handled">AI Handled</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Conversations List */}
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                    {isLoading ? (
                        <div className="text-center py-12">
                            <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
                            <p className="text-gray-500 mt-4">Loading conversations...</p>
                        </div>
                    ) : filteredConversations.length === 0 ? (
                        <div className="text-center py-12">
                            <MessageSquare className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <p className="text-gray-500">No conversations found</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {filteredConversations.map((conv) => (
                                <div
                                    key={conv.patient.id}
                                    onClick={() => navigate(`/staff/messages/${conv.patient.id}`)}
                                    className="p-4 bg-gray-50 rounded-xl hover:bg-blue-50 transition-colors cursor-pointer group"
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-3 mb-2">
                                                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                                                    {conv.patient.name.charAt(0).toUpperCase()}
                                                </div>
                                                <div>
                                                    <div className="flex items-center gap-2">
                                                        <span className="font-semibold text-gray-900">{conv.patient.name}</span>
                                                        {conv.unreadCount > 0 && (
                                                            <span className="px-2 py-1 bg-red-500 text-white text-xs rounded-full">
                                                                {conv.unreadCount}
                                                            </span>
                                                        )}
                                                    </div>
                                                    <span className="text-sm text-gray-500">{conv.patient.phone}</span>
                                                </div>
                                            </div>

                                            {conv.lastMessage && (
                                                <div className="ml-13">
                                                    <div className="flex items-center gap-2 mb-1">
                                                        {conv.lastMessage.is_ai_handled && (
                                                            <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full flex items-center gap-1">
                                                                <Bot className="w-3 h-3" />
                                                                AI
                                                            </span>
                                                        )}
                                                        {conv.lastMessage.needs_human && (
                                                            <span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full flex items-center gap-1">
                                                                <AlertCircle className="w-3 h-3" />
                                                                Needs Attention
                                                            </span>
                                                        )}
                                                        <span className="text-xs text-gray-400 flex items-center gap-1">
                                                            <Clock className="w-3 h-3" />
                                                            {new Date(conv.lastMessage.created_at).toLocaleString()}
                                                        </span>
                                                    </div>
                                                    <p className="text-sm text-gray-600 line-clamp-2">
                                                        {conv.lastMessage.content}
                                                    </p>
                                                </div>
                                            )}
                                        </div>

                                        <div className="flex items-center gap-3 ml-4">
                                            <div className="text-right">
                                                <div className="text-sm font-medium text-gray-700">
                                                    {conv.messages.length} messages
                                                </div>
                                                <div className="text-xs text-gray-500">
                                                    {conv.patient.preferred_language.toUpperCase()}
                                                </div>
                                            </div>
                                            <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors" />
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Stats Summary */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                    <div className="bg-white rounded-xl p-4 shadow border border-gray-100">
                        <div className="flex items-center gap-3">
                            <MessageSquare className="w-8 h-8 text-blue-500" />
                            <div>
                                <p className="text-sm text-gray-600">Total Conversations</p>
                                <p className="text-2xl font-bold text-gray-900">{patientConversations.length}</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl p-4 shadow border border-gray-100">
                        <div className="flex items-center gap-3">
                            <Bot className="w-8 h-8 text-green-500" />
                            <div>
                                <p className="text-sm text-gray-600">AI Handled</p>
                                <p className="text-2xl font-bold text-gray-900">
                                    {patientConversations.filter(c => c.messages.every(m => m.is_ai_handled)).length}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl p-4 shadow border border-gray-100">
                        <div className="flex items-center gap-3">
                            <AlertCircle className="w-8 h-8 text-red-500" />
                            <div>
                                <p className="text-sm text-gray-600">Needs Attention</p>
                                <p className="text-2xl font-bold text-gray-900">
                                    {patientConversations.filter(c => c.messages.some(m => m.needs_human)).length}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
