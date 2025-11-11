import React, { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  usePatient, 
  useMessagesByPatient,
  useLiveMessages,
  useCreateMessage,
  useUpdateMessage 
} from '../hooks/useApi'
import { 
  ArrowLeft, 
  Send, 
  Bot, 
  AlertCircle, 
  User,
  Phone,
  Globe,
  Calendar,
  MessageSquare,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react'
import { formatDate, getChannelIcon, getLanguageFlag, getLanguageName, getConfidenceColor } from '../utils/helpers'
import { Message } from '../types'

const PatientDetails: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>()
  const navigate = useNavigate()
  const [newMessage, setNewMessage] = useState('')
  const [isHumanIntervention, setIsHumanIntervention] = useState(false)

  const patientIdNum = parseInt(patientId || '0', 10)

  // Fetch patient data and messages
  const { data: patient, isLoading: patientLoading } = usePatient(patientIdNum)
  const { data: historicalMessages = [] } = useMessagesByPatient(patientIdNum)
  const { messages: liveMessages, refresh, lastUpdate, isLoading: messagesLoading } = useLiveMessages(patientIdNum)

  // Combine historical and live messages
  const allMessages = [...historicalMessages, ...liveMessages].sort((a, b) => 
    new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  )

  const createMessageMutation = useCreateMessage()
  const updateMessageMutation = useUpdateMessage()

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !patient) return

    try {
      await createMessageMutation.mutateAsync({
        patient: patient.id,
        content: newMessage,
        direction: 'outgoing',
        channel: 'sms', // Default channel for staff responses
        is_ai_handled: false,
        needs_human: false,
      })

      setNewMessage('')
      refresh()
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  const handleHumanIntervention = async (messageId: number) => {
    try {
      await updateMessageMutation.mutateAsync({
        id: messageId,
        data: { needs_human: true }
      })
      refresh()
    } catch (error) {
      console.error('Failed to flag for human intervention:', error)
    }
  }

  const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
    const isIncoming = message.direction === 'incoming'
    
    return (
      <div className={`flex ${isIncoming ? 'justify-start' : 'justify-end'} mb-4`}>
        <div className={`max-w-xs lg:max-w-md ${
          isIncoming ? 'order-2' : 'order-1'
        }`}>
          <div className={`flex items-center mb-1 ${
            isIncoming ? 'justify-start' : 'justify-end'
          }`}>
            <div className={`flex items-center space-x-2 ${
              isIncoming ? 'order-1' : 'order-2'
            }`}>
              <span className="text-xs text-gray-500">
                {formatDate(message.created_at)}
              </span>
              <span className="text-xs">
                {getChannelIcon(message.channel)}
              </span>
            </div>
          </div>
          
          <div className={`px-4 py-2 rounded-lg ${
            isIncoming 
              ? 'bg-gray-100 text-gray-800' 
              : 'bg-healthcare-primary text-white'
          }`}>
            <p className="text-sm">{message.content}</p>
          </div>
          
          {/* Message Status and Actions */}
          <div className={`flex items-center space-x-2 mt-1 ${
            isIncoming ? 'justify-start' : 'justify-end'
          }`}>
            {message.is_ai_handled && (
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getConfidenceColor(message.confidence_score)}`}>
                <Bot className="h-3 w-3 mr-1" />
                AI ({Math.round((message.confidence_score || 0) * 100)}%)
              </span>
            )}
            
            {message.needs_human && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                <AlertTriangle className="h-3 w-3 mr-1" />
                Human Needed
              </span>
            )}
            
            {isIncoming && message.needs_human && (
              <button
                onClick={() => handleHumanIntervention(message.id)}
                className="text-xs text-red-600 hover:text-red-800 underline"
              >
                Mark as Handled
              </button>
            )}
          </div>
        </div>
      </div>
    )
  }

  if (patientLoading || messagesLoading) {
    return (
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-healthcare-primary"></div>
        </div>
      </div>
    )
  }

  if (!patient) {
    return (
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900">Patient not found</h3>
          <button
            onClick={() => navigate('/staff/messages')}
            className="mt-4 btn-primary"
          >
            Back to Messages
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/staff/messages')}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {patient.name || 'Unknown Patient'}
              </h1>
              <p className="text-gray-600">Patient Conversation</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <button
              onClick={refresh}
              className="btn-secondary"
              disabled={messagesLoading}
            >
              <Clock className="h-4 w-4 mr-2" />
              Refresh
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Patient Sidebar */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-healthcare-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <User className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                {patient.name || 'Unknown Patient'}
              </h3>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">Phone</p>
                  <p className="text-sm font-medium">{patient.phone}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Globe className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">Preferred Language</p>
                  <p className="text-sm font-medium">
                    {getLanguageFlag(patient.preferred_language)} {getLanguageName(patient.preferred_language)}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Calendar className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">Member Since</p>
                  <p className="text-sm font-medium">{formatDate(patient.created_at)}</p>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Conversation Stats</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Total Messages</span>
                  <span className="text-sm font-medium">{allMessages.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">AI Handled</span>
                  <span className="text-sm font-medium">
                    {allMessages.filter(m => m.is_ai_handled).length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Human Required</span>
                  <span className="text-sm font-medium text-red-600">
                    {allMessages.filter(m => m.needs_human).length}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="lg:col-span-3">
          <div className="card h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5 text-healthcare-primary" />
                <span className="font-medium">Conversation History</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-500">
                  Last updated: {formatDate(lastUpdate.toISOString())}
                </span>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {allMessages.length > 0 ? (
                allMessages.map((message) => (
                  <MessageBubble key={message.id} message={message} />
                ))
              ) : (
                <div className="text-center py-12">
                  <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No messages yet</p>
                </div>
              )}
            </div>

            {/* Message Input */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex items-end space-x-2">
                <div className="flex-1">
                  <textarea
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent resize-none"
                    rows={2}
                    placeholder="Type a response..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault()
                        handleSendMessage()
                      }
                    }}
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={!newMessage.trim() || createMessageMutation.isLoading}
                  className="btn-primary p-2"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
              
              <div className="flex items-center justify-between mt-2">
                <button
                  onClick={() => setIsHumanIntervention(!isHumanIntervention)}
                  className={`text-sm ${isHumanIntervention ? 'text-red-600' : 'text-gray-500'} hover:underline`}
                >
                  {isHumanIntervention ? 'Human intervention active' : 'Flag for human intervention'}
                </button>
                <span className="text-xs text-gray-500">
                  Press Enter to send, Shift+Enter for new line
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PatientDetails