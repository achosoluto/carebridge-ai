import React, { useState } from 'react'
import {
  useSystemMetrics,
  useSystemMetricsSummary,
  useRealTimeUpdates
} from '../hooks/useApi'
import { HealthService } from '../services/apiServices'
import { 
  Activity,
  MessageSquare,
  Bot,
  Clock,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Server,
  Database,
  Wifi,
  Zap,
  BarChart3
} from 'lucide-react'
import { formatDate, formatRelativeTime } from '../utils/helpers'

const Monitoring: React.FC = () => {
  console.log('Rendering Monitoring');
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [healthStatus, setHealthStatus] = useState<any>(null)
  
  // Fetch data
  const { data: metrics = [], isLoading: metricsLoading } = useSystemMetrics()
  const { data: summary } = useSystemMetricsSummary()
  const { isConnected } = useRealTimeUpdates()

  const handleRefresh = async () => {
    setIsRefreshing(true)
    try {
      const health = await HealthService.check()
      setHealthStatus(health)
    } catch (error) {
      console.error('Failed to fetch health status:', error)
    } finally {
      setIsRefreshing(false)
    }
  }

  React.useEffect(() => {
    handleRefresh()
  }, [])

  const MetricCard: React.FC<{
    title: string
    value: string | number
    icon: React.ComponentType<any>
    color: string
    change?: string
    trend?: 'up' | 'down' | 'neutral'
  }> = ({ title, value, icon: Icon, color, change, trend }) => (
    <div className="card">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`p-3 rounded-lg ${color}`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
            {change && (
              <div className="flex items-center mt-1">
                {trend === 'up' && <TrendingUp className="h-4 w-4 text-green-500 mr-1" />}
                {trend === 'down' && <TrendingDown className="h-4 w-4 text-red-500 mr-1" />}
                <p className={`text-sm ${trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-600'}`}>
                  {change}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )

  const ServiceStatus: React.FC<{ name: string; status: string; description?: string }> = ({ 
    name, 
    status, 
    description 
  }) => {
    const getStatusIcon = () => {
      switch (status) {
        case 'healthy': return <CheckCircle className="h-5 w-5 text-green-500" />
        case 'unhealthy': return <XCircle className="h-5 w-5 text-red-500" />
        default: return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      }
    }

    const getStatusColor = () => {
      switch (status) {
        case 'healthy': return 'bg-green-100 text-green-800'
        case 'unhealthy': return 'bg-red-100 text-red-800'
        default: return 'bg-yellow-100 text-yellow-800'
      }
    }

    return (
      <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <p className="font-medium text-gray-900">{name}</p>
            {description && (
              <p className="text-sm text-gray-600">{description}</p>
            )}
          </div>
        </div>
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor()}`}>
          {status}
        </span>
      </div>
    )
  }

  if (metricsLoading) {
    return (
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-healthcare-primary"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">System Monitoring</h1>
            <p className="text-gray-600">Monitor system performance and health status</p>
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
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="btn-primary"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Total Messages"
          value={summary?.total_messages || 0}
          icon={MessageSquare}
          color="bg-blue-500"
          change="+12% this week"
          trend="up"
        />
        <MetricCard
          title="AI Handled"
          value={summary?.ai_handled || 0}
          icon={Bot}
          color="bg-green-500"
          change={`${summary?.total_messages ? Math.round((summary.ai_handled / summary.total_messages) * 100) : 0}% rate`}
          trend="up"
        />
        <MetricCard
          title="Human Required"
          value={summary?.human_required || 0}
          icon={AlertTriangle}
          color="bg-red-500"
          change="Needs attention"
          trend="down"
        />
        <MetricCard
          title="Avg Response Time"
          value="1.2s"
          icon={Clock}
          color="bg-purple-500"
          change="-0.3s improvement"
          trend="up"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* System Health */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">System Health</h2>
              <Activity className="h-5 w-5 text-healthcare-primary" />
            </div>
            
            <div className="space-y-4">
              <ServiceStatus
                name="Database"
                status={healthStatus?.services?.database || 'checking'}
                description="PostgreSQL connection"
              />
              <ServiceStatus
                name="Redis Cache"
                status={healthStatus?.services?.redis || 'not_configured'}
                description="Caching layer"
              />
              <ServiceStatus
                name="AI Service"
                status={healthStatus?.services?.ai_service || 'not_configured'}
                description="OpenAI integration"
              />
              <ServiceStatus
                name="API Gateway"
                status="healthy"
                description="Django REST framework"
              />
              <ServiceStatus
                name="Frontend"
                status={isConnected ? 'healthy' : 'unhealthy'}
                description="React application"
              />
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">System Uptime</span>
                <span className="text-sm text-green-600">99.9%</span>
              </div>
              <div className="mt-2 bg-gray-200 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '99.9%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Performance Metrics</h2>
              <BarChart3 className="h-5 w-5 text-healthcare-primary" />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Channel Performance */}
              <div>
                <h3 className="text-sm font-medium text-gray-900 mb-4">Channel Performance</h3>
                <div className="space-y-3">
                  {[
                    { name: 'SMS', messages: 60, success: 95, icon: '📱' },
                  ].map((channel) => (
                    <div key={channel.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">{channel.icon}</span>
                        <div>
                          <p className="text-sm font-medium">{channel.name}</p>
                          <p className="text-xs text-gray-600">{channel.messages} messages</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium">{channel.success}%</p>
                        <div className="w-16 bg-gray-200 rounded-full h-1">
                          <div 
                            className={`h-1 rounded-full ${
                              channel.success >= 95 ? 'bg-green-500' : 
                              channel.success >= 90 ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${channel.success}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Language Distribution */}
              <div>
                <h3 className="text-sm font-medium text-gray-900 mb-4">Language Distribution</h3>
                <div className="space-y-3">
                  {[
                    { language: 'Korean', percentage: 60, count: 72, flag: '🇰🇷' },
                    { language: 'English', percentage: 40, count: 48, flag: '🇺🇸' },
                  ].map((lang) => (
                    <div key={lang.language} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">{lang.flag}</span>
                        <div>
                          <p className="text-sm font-medium">{lang.language}</p>
                          <p className="text-xs text-gray-600">{lang.count} messages</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium">{lang.percentage}%</p>
                        <div className="w-16 bg-gray-200 rounded-full h-1">
                          <div 
                            className="bg-healthcare-primary h-1 rounded-full"
                            style={{ width: `${lang.percentage}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Recent Metrics Table */}
            <div className="mt-8">
              <h3 className="text-sm font-medium text-gray-900 mb-4">Recent Metrics</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total Messages
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        AI Handled
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Human Required
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Response Time
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {metrics.slice(0, 7).map((metric) => (
                      <tr key={metric.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatDate(metric.date)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {metric.total_messages}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">
                          {metric.ai_handled_messages}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                          {metric.human_needed_messages}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {metric.average_response_time ? 
                            `${Math.round(parseFloat(metric.average_response_time) / 1000)}s` : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* System Alerts */}
      <div className="mt-8">
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">System Alerts</h2>
            <AlertTriangle className="h-5 w-5 text-yellow-500" />
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <AlertTriangle className="h-5 w-5 text-yellow-500 mr-3" />
              <div>
                <p className="text-sm font-medium text-yellow-800">SMS Channel Degradation</p>
                <p className="text-xs text-yellow-700">SMS delivery rate dropped to 89% - below 95% threshold</p>
              </div>
              <span className="ml-auto text-xs text-yellow-600">
                {formatRelativeTime(new Date().toISOString())}
              </span>
            </div>
            
            <div className="flex items-center p-3 bg-green-50 border border-green-200 rounded-lg">
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              <div>
                <p className="text-sm font-medium text-green-800">All Systems Operational</p>
                <p className="text-xs text-green-700">All services are running normally</p>
              </div>
              <span className="ml-auto text-xs text-green-600">
                Last checked {formatRelativeTime(new Date().toISOString())}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Monitoring