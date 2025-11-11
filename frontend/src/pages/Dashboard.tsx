import React from 'react'
import { useRealTimeUpdates } from '../hooks/useApi'
import { 
  MessageSquare, 
  Users, 
  Calendar, 
  Activity,
  TrendingUp,
  Clock,
  Bot,
  AlertCircle,
  CheckCircle,
  RefreshCw
} from 'lucide-react'
import { formatRelativeTime, getChannelIcon, getConfidenceColor, getLanguageFlag } from '../utils/helpers'

const Dashboard: React.FC = () => {
  const { isConnected, messages, systemMetrics } = useRealTimeUpdates()

  // Get recent messages (last 10)
  const recentMessages = messages.slice(0, 10)

  // Calculate stats
  const stats = {
    totalMessages: messages.length,
    todayMessages: messages.filter(msg => {
      const today = new Date().toDateString()
      return new Date(msg.created_at).toDateString() === today
    }).length,
    aiHandled: messages.filter(msg => msg.is_ai_handled).length,
    needsHuman: messages.filter(msg => msg.needs_human).length,
  }

  const MetricCard: React.FC<{
    title: string
    value: number
    icon: React.ComponentType<any>
    color: string
    change?: string
  }> = ({ title, value, icon: Icon, color, change }) => (
    <div className="card">
      <div className="flex items-center">
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {change && (
            <p className="text-sm text-green-600">{change}</p>
          )}
        </div>
      </div>
    </div>
  )

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Staff Dashboard</h1>
            <p className="text-gray-600">Monitor patient communications and system performance</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
              isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              <div className={`h-2 w-2 rounded-full ${
                isConnected ? 'bg-green-500' : 'bg-red-500'
              }`} />
              <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
            <button className="btn-secondary">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Total Messages"
          value={stats.totalMessages}
          icon={MessageSquare}
          color="bg-blue-500"
          change="+12% today"
        />
        <MetricCard
          title="AI Handled"
          value={stats.aiHandled}
          icon={Bot}
          color="bg-green-500"
        />
        <MetricCard
          title="Needs Human"
          value={stats.needsHuman}
          icon={AlertCircle}
          color="bg-red-500"
        />
        <MetricCard
          title="System Status"
          value={98}
          icon={Activity}
          color="bg-purple-500"
          change="98% uptime"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Messages */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Recent Messages</h2>
              <span className="text-sm text-gray-500">Last 10 messages</span>
            </div>
            
            <div className="space-y-4">
              {recentMessages.map((message) => (
                <div key={message.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                      <span className="text-sm font-medium">
                        {getLanguageFlag(message.patient_name || 'ko')}
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-gray-900">
                        {message.patient_name || 'Unknown Patient'}
                      </p>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-500">
                          {formatRelativeTime(message.created_at)}
                        </span>
                        <span className="text-xs">
                          {getChannelIcon(message.channel)}
                        </span>
                      </div>
                    </div>
                    
                    <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                      {message.content}
                    </p>
                    
                    <div className="flex items-center space-x-2 mt-2">
                      {message.is_ai_handled && (
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getConfidenceColor(message.confidence_score)}`}>
                          <Bot className="h-3 w-3 mr-1" />
                          AI ({Math.round((message.confidence_score || 0) * 100)}%)
                        </span>
                      )}
                      {message.needs_human && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                          <AlertCircle className="h-3 w-3 mr-1" />
                          Needs Human
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              
              {recentMessages.length === 0 && (
                <div className="text-center py-8">
                  <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No recent messages</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions & System Status */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full btn-primary">
                <Users className="h-4 w-4 mr-2" />
                View All Patients
              </button>
              <button className="w-full btn-secondary">
                <Calendar className="h-4 w-4 mr-2" />
                Schedule Appointment
              </button>
              <button className="w-full btn-secondary">
                <TrendingUp className="h-4 w-4 mr-2" />
                View Reports
              </button>
            </div>
          </div>

          {/* System Performance */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">System Performance</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm">
                  <span>AI Accuracy</span>
                  <span>92%</span>
                </div>
                <div className="mt-1 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '92%' }} />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm">
                  <span>Response Time</span>
                  <span>1.2s</span>
                </div>
                <div className="mt-1 bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: '85%' }} />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm">
                  <span>Uptime</span>
                  <span>99.9%</span>
                </div>
                <div className="mt-1 bg-gray-200 rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{ width: '99.9%' }} />
                </div>
              </div>
            </div>
          </div>

          {/* Channel Status */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Channel Status</h3>
            <div className="space-y-3">
              {[
                { name: 'KakaoTalk', icon: '💬', status: 'active' },
                { name: 'WeChat', icon: '💚', status: 'active' },
                { name: 'LINE', icon: '🟢', status: 'active' },
                { name: 'SMS', icon: '📱', status: 'maintenance' },
              ].map((channel) => (
                <div key={channel.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span>{channel.icon}</span>
                    <span className="text-sm">{channel.name}</span>
                  </div>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    channel.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {channel.status === 'active' ? (
                      <CheckCircle className="h-3 w-3 mr-1" />
                    ) : (
                      <Clock className="h-3 w-3 mr-1" />
                    )}
                    {channel.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard