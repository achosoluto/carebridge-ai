import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { usePatients, useMessages, useRealTimeUpdates } from '../hooks/useApi'
import { 
  Search, 
  MessageSquare, 
  Phone, 
  Clock,
  Bot,
  AlertCircle,
  Filter,
  User,
  ArrowRight
} from 'lucide-react'
import { formatRelativeTime, getChannelIcon, getLanguageFlag, getLanguageName, getConfidenceColor } from '../utils/helpers'
import { Patient, Message } from '../types'

const Messages: React.FC = () => {
  console.log('Rendering Messages');
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState<'all' | 'needs-human' | 'ai-handled'>('all')

  // Fetch data
  const { data: patients = [], isLoading: patientsLoading } = usePatients()
  const { data: messages = [], isLoading: messagesLoading } = useMessages()
  const { isConnected } = useRealTimeUpdates()

  // Group messages by patient for conversation list
  const messagesByPatient = React.useMemo(() => {
    const grouped = messages.reduce((acc, message) => {
      if (!acc[message.patient]) {
        acc[message.patient] = {
          patient: patients.find(p => p.id === message.patient) || { 
            id: message.patient, 
            name: message.patient_name, 
            phone: message.patient_phone,
            preferred_language: 'ko' as const,
            created_at: '',
            updated_at: ''
          },
          messages: []
        }
      }
      acc[message.patient].messages.push(message)
      return acc
    }, {} as Record<number, { patient: Patient; messages: Message[] }>)
    
    return Object.values(grouped)
  }, [messages, patients])

  // Filter conversations based on search and status
  const filteredConversations = messagesByPatient.filter(({ patient, messages }) => {
    const matchesSearch = patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         patient.phone.includes(searchTerm)
    
    if (!matchesSearch) return false

    const latestMessage = messages[0] // Messages are ordered by -created_at
    switch (filterStatus) {
      case 'needs-human':
        return latestMessage?.needs_human
      case 'ai-handled':
        return latestMessage?.is_ai_handled && !latestMessage?.needs_human
      default:
        return true
    }
  })

  // Sort conversations by latest message
  const sortedConversations = filteredConversations.sort((a, b) => {
    const aLatest = a.messages[0]?.created_at || ''
    const bLatest = b.messages[0]?.created_at || ''
    return new Date(bLatest).getTime() - new Date(aLatest).getTime()
  })

  const ConversationCard: React.FC<{ conversation: { patient: Patient; messages: Message[] } }> = ({ 
    conversation 
  }) => {
    const { patient, messages } = conversation
    const latestMessage = messages[0]
    const unreadCount = messages.filter(m => m.direction === 'incoming').length

    return (
      <div 
        className="card hover:shadow-md transition-shadow cursor-pointer"
        onClick={() => navigate(`/staff/messages/${patient.id}`)}
      >
        <div className="flex items-start space-x-4">
          {/* Patient Avatar */}
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-healthcare-primary rounded-full flex items-center justify-center">
              <User className="h-6 w-6 text-white" />
            </div>
            <div className="text-center mt-1">
              <span className="text-xs">{getLanguageFlag(patient.preferred_language)}</span>
            </div>
          </div>

          {/* Conversation Details */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-gray-900 truncate">
                {patient.name || 'Unknown Patient'}
              </h3>
              <div className="flex items-center space-x-2">
                {unreadCount > 0 && (
                  <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-medium text-white bg-red-500 rounded-full">
                    {unreadCount}
                  </span>
                )}
                <span className="text-xs text-gray-500">
                  {formatRelativeTime(latestMessage?.created_at || patient.updated_at)}
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-2 mt-1">
              <span className="text-sm text-gray-600">{patient.phone}</span>
              <span className="text-xs text-gray-500">•</span>
              <span className="text-xs text-gray-500">
                {getLanguageName(patient.preferred_language)}
              </span>
            </div>

            {/* Latest Message Preview */}
            {latestMessage && (
              <div className="mt-2">
                <div className="flex items-center space-x-2">
                  <span className="text-xs">
                    {getChannelIcon(latestMessage.channel)}
                  </span>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    latestMessage.direction === 'incoming' 
                      ? 'bg-gray-100 text-gray-700' 
                      : 'bg-healthcare-primary text-white'
                  }`}>
                    {latestMessage.direction === 'incoming' ? 'Patient' : 'You'}
                  </span>
                  
                  {latestMessage.is_ai_handled && (
                    <span className={`text-xs px-2 py-1 rounded-full ${getConfidenceColor(latestMessage.confidence_score)}`}>
                      <Bot className="h-3 w-3 inline mr-1" />
                      AI
                    </span>
                  )}
                  
                  {latestMessage.needs_human && (
                    <span className="text-xs px-2 py-1 rounded-full bg-red-100 text-red-800">
                      <AlertCircle className="h-3 w-3 inline mr-1" />
                      Human Needed
                    </span>
                  )}
                </div>
                
                <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                  {latestMessage.content}
                </p>
              </div>
            )}
          </div>

          {/* Action Arrow */}
          <div className="flex-shrink-0">
            <ArrowRight className="h-5 w-5 text-gray-400" />
          </div>
        </div>
      </div>
    )
  }

  if (patientsLoading || messagesLoading) {
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
            <h1 className="text-2xl font-bold text-gray-900">Patient Messages</h1>
            <p className="text-gray-600">Monitor and manage patient conversations</p>
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
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="card mb-6">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search patients by name or phone..."
                className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          {/* Status Filter */}
          <div className="sm:w-48">
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value as 'all' | 'needs-human' | 'ai-handled')}
            >
              <option value="all">All Conversations</option>
              <option value="needs-human">Needs Human</option>
              <option value="ai-handled">AI Handled</option>
            </select>
          </div>
        </div>
      </div>

      {/* Conversations List */}
      <div className="space-y-4">
        {sortedConversations.length > 0 ? (
          sortedConversations.map((conversation) => (
            <ConversationCard key={conversation.patient.id} conversation={conversation} />
          ))
        ) : (
          <div className="card text-center py-12">
            <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No conversations found</h3>
            <p className="text-gray-600">
              {searchTerm || filterStatus !== 'all' 
                ? 'Try adjusting your search or filter criteria' 
                : 'No patient conversations available yet'}
            </p>
          </div>
        )}
      </div>

      {/* Statistics Footer */}
      {sortedConversations.length > 0 && (
        <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="card text-center">
            <div className="text-2xl font-bold text-healthcare-primary">{sortedConversations.length}</div>
            <div className="text-sm text-gray-600">Total Conversations</div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-blue-600">
              {sortedConversations.filter(c => c.messages[0]?.is_ai_handled).length}
            </div>
            <div className="text-sm text-gray-600">AI Handled</div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-red-600">
              {sortedConversations.filter(c => c.messages[0]?.needs_human).length}
            </div>
            <div className="text-sm text-gray-600">Needs Human</div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Messages