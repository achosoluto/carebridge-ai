import { useRealTimeUpdates } from '../hooks/useApi'
import { MessageSquare, Users, Bot, Activity } from 'lucide-react'

export default function Dashboard() {
    const { isConnected, messages } = useRealTimeUpdates()

    const stats = {
        totalMessages: messages.length,
        aiHandled: messages.filter(m => m.is_ai_handled).length,
        needsHuman: messages.filter(m => m.needs_human).length,
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2">CareBridge AI Dashboard</h1>
                    <p className="text-gray-600 mb-4">Monitor patient communications and system performance</p>

                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white shadow-sm border border-gray-200">
                        <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
                        <span className="text-sm font-medium">{isConnected ? 'Connected' : 'Disconnected'}</span>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-blue-100 rounded-xl">
                                <MessageSquare className="w-8 h-8 text-blue-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Total Messages</p>
                                <p className="text-3xl font-bold text-gray-900">{stats.totalMessages}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-green-100 rounded-xl">
                                <Bot className="w-8 h-8 text-green-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">AI Handled</p>
                                <p className="text-3xl font-bold text-gray-900">{stats.aiHandled}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-red-100 rounded-xl">
                                <Users className="w-8 h-8 text-red-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Needs Human</p>
                                <p className="text-3xl font-bold text-gray-900">{stats.needsHuman}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Recent Messages */}
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Messages</h2>

                    {messages.length === 0 ? (
                        <div className="text-center py-12">
                            <MessageSquare className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <p className="text-gray-500">No messages yet</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {messages.slice(0, 10).map((message) => (
                                <div key={message.id} className="p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <span className="font-medium text-gray-900">{message.patient_name || 'Unknown'}</span>
                                                {message.is_ai_handled && (
                                                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full flex items-center gap-1">
                                                        <Bot className="w-3 h-3" />
                                                        AI {message.confidence_score && `(${Math.round(message.confidence_score * 100)}%)`}
                                                    </span>
                                                )}
                                                {message.needs_human && (
                                                    <span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full flex items-center gap-1">
                                                        <Activity className="w-3 h-3" />
                                                        Human Needed
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-sm text-gray-600 line-clamp-2">{message.content}</p>
                                            <p className="text-xs text-gray-400 mt-1">
                                                {new Date(message.created_at).toLocaleString()} • {message.channel}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
