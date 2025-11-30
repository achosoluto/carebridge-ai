import { useRealTimeUpdates } from '../hooks/useApi'
import { Activity, Zap, Clock, TrendingUp, AlertCircle, CheckCircle, MessageSquare, Users } from 'lucide-react'

export default function Monitoring() {
    const { isConnected, messages, systemMetrics } = useRealTimeUpdates()

    const stats = {
        totalMessages: messages.length,
        aiHandled: messages.filter(m => m.is_ai_handled).length,
        needsHuman: messages.filter(m => m.needs_human).length,
        avgConfidence: messages.filter(m => m.confidence_score).reduce((acc, m) => acc + (m.confidence_score || 0), 0) / messages.filter(m => m.confidence_score).length || 0
    }

    const channelStats = {
        kakao: messages.filter(m => m.channel === 'kakao').length,
        wechat: messages.filter(m => m.channel === 'wechat').length,
        line: messages.filter(m => m.channel === 'line').length,
        sms: messages.filter(m => m.channel === 'sms').length
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2">System Monitoring</h1>
                    <p className="text-gray-600 mb-4">Real-time system performance and metrics</p>

                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white shadow-sm border border-gray-200">
                        <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
                        <span className="text-sm font-medium">{isConnected ? 'System Online' : 'System Offline'}</span>
                    </div>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="p-3 bg-blue-100 rounded-xl">
                                <MessageSquare className="w-6 h-6 text-blue-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Total Messages</p>
                                <p className="text-3xl font-bold text-gray-900">{stats.totalMessages}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-1 text-sm text-green-600">
                            <TrendingUp className="w-4 h-4" />
                            <span>Active</span>
                        </div>
                    </div>

                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="p-3 bg-green-100 rounded-xl">
                                <CheckCircle className="w-6 h-6 text-green-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">AI Handled</p>
                                <p className="text-3xl font-bold text-gray-900">{stats.aiHandled}</p>
                            </div>
                        </div>
                        <div className="text-sm text-gray-500">
                            {stats.totalMessages > 0 ? Math.round((stats.aiHandled / stats.totalMessages) * 100) : 0}% automation rate
                        </div>
                    </div>

                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="p-3 bg-red-100 rounded-xl">
                                <AlertCircle className="w-6 h-6 text-red-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Needs Human</p>
                                <p className="text-3xl font-bold text-gray-900">{stats.needsHuman}</p>
                            </div>
                        </div>
                        <div className="text-sm text-gray-500">
                            {stats.totalMessages > 0 ? Math.round((stats.needsHuman / stats.totalMessages) * 100) : 0}% escalation rate
                        </div>
                    </div>

                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="p-3 bg-purple-100 rounded-xl">
                                <Zap className="w-6 h-6 text-purple-600" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Avg Confidence</p>
                                <p className="text-3xl font-bold text-gray-900">
                                    {Math.round(stats.avgConfidence * 100)}%
                                </p>
                            </div>
                        </div>
                        <div className="text-sm text-gray-500">
                            AI confidence score
                        </div>
                    </div>
                </div>

                {/* Channel Distribution */}
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Channel Distribution</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {Object.entries(channelStats).map(([channel, count]) => (
                            <div key={channel} className="p-4 bg-gray-50 rounded-xl">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium text-gray-700 capitalize">{channel}</span>
                                    <span className="text-2xl font-bold text-gray-900">{count}</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div
                                        className="bg-blue-500 h-2 rounded-full transition-all"
                                        style={{ width: `${stats.totalMessages > 0 ? (count / stats.totalMessages) * 100 : 0}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* System Performance */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4">System Performance</h2>
                        <div className="space-y-4">
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <Activity className="w-5 h-5 text-blue-500" />
                                    <span className="text-sm font-medium text-gray-700">Response Time</span>
                                </div>
                                <span className="text-sm font-bold text-gray-900">&lt;100ms</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <Clock className="w-5 h-5 text-green-500" />
                                    <span className="text-sm font-medium text-gray-700">Uptime</span>
                                </div>
                                <span className="text-sm font-bold text-gray-900">99.9%</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <Zap className="w-5 h-5 text-purple-500" />
                                    <span className="text-sm font-medium text-gray-700">Processing Rate</span>
                                </div>
                                <span className="text-sm font-bold text-gray-900">{stats.totalMessages}/min</span>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
                        <div className="space-y-3">
                            {messages.slice(0, 5).map((message) => (
                                <div key={message.id} className="p-3 bg-gray-50 rounded-lg">
                                    <div className="flex items-center justify-between mb-1">
                                        <span className="text-sm font-medium text-gray-900">{message.patient_name || 'Unknown'}</span>
                                        <span className="text-xs text-gray-500">{message.channel}</span>
                                    </div>
                                    <p className="text-xs text-gray-600 line-clamp-1">{message.content}</p>
                                    <div className="flex items-center gap-2 mt-1">
                                        {message.is_ai_handled && (
                                            <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">AI</span>
                                        )}
                                        {message.needs_human && (
                                            <span className="text-xs px-2 py-0.5 bg-red-100 text-red-700 rounded-full">Human</span>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
