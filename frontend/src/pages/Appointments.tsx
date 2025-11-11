import React, { useState } from 'react'
import { 
  useAppointments, 
  usePatients,
  useCreateAppointment,
  useUpdateAppointment,
  useDeleteAppointment
} from '../hooks/useApi'
import { 
  Calendar,
  Plus,
  Clock,
  User,
  Phone,
  CheckCircle,
  XCircle,
  AlertCircle,
  Edit,
  Trash2,
  Filter,
  Search
} from 'lucide-react'
import { formatDate, getStatusColor, formatRelativeTime } from '../utils/helpers'
import { Appointment, AppointmentFormData } from '../types'

const Appointments: React.FC = () => {
  const [showForm, setShowForm] = useState(false)
  const [editingAppointment, setEditingAppointment] = useState<Appointment | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [dateFilter, setDateFilter] = useState<string>('upcoming')

  // Form state
  const [formData, setFormData] = useState<AppointmentFormData>({
    patient_id: 0,
    doctor: '',
    procedure: '',
    scheduled_at: '',
    notes: ''
  })

  // Fetch data
  const { data: appointments = [], isLoading: appointmentsLoading } = useAppointments()
  const { data: patients = [] } = usePatients()
  const createMutation = useCreateAppointment()
  const updateMutation = useUpdateAppointment()
  const deleteMutation = useDeleteAppointment()

  // Filter appointments
  const filteredAppointments = React.useMemo(() => {
    let filtered = appointments

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(apt => 
        apt.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        apt.doctor.toLowerCase().includes(searchTerm.toLowerCase()) ||
        apt.procedure.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(apt => apt.status === statusFilter)
    }

    // Date filter
    const now = new Date()
    if (dateFilter === 'upcoming') {
      filtered = filtered.filter(apt => new Date(apt.scheduled_at) > now)
    } else if (dateFilter === 'today') {
      filtered = filtered.filter(apt => {
        const aptDate = new Date(apt.scheduled_at)
        return aptDate.toDateString() === now.toDateString()
      })
    } else if (dateFilter === 'past') {
      filtered = filtered.filter(apt => new Date(apt.scheduled_at) < now)
    }

    return filtered.sort((a, b) => new Date(a.scheduled_at).getTime() - new Date(b.scheduled_at).getTime())
  }, [appointments, searchTerm, statusFilter, dateFilter])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (editingAppointment) {
        await updateMutation.mutateAsync({
          id: editingAppointment.id,
          data: formData
        })
      } else {
        await createMutation.mutateAsync(formData)
      }
      
      setShowForm(false)
      setEditingAppointment(null)
      setFormData({
        patient_id: 0,
        doctor: '',
        procedure: '',
        scheduled_at: '',
        notes: ''
      })
    } catch (error) {
      console.error('Failed to save appointment:', error)
    }
  }

  const handleEdit = (appointment: Appointment) => {
    setEditingAppointment(appointment)
    setFormData({
      patient_id: appointment.patient,
      doctor: appointment.doctor,
      procedure: appointment.procedure,
      scheduled_at: appointment.scheduled_at,
      notes: appointment.notes
    })
    setShowForm(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this appointment?')) {
      try {
        await deleteMutation.mutateAsync(id)
      } catch (error) {
        console.error('Failed to delete appointment:', error)
      }
    }
  }

  const handleStatusChange = async (id: number, status: string) => {
    try {
      await updateMutation.mutateAsync({
        id,
        data: { status }
      })
    } catch (error) {
      console.error('Failed to update status:', error)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'confirmed': return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'cancelled': return <XCircle className="h-4 w-4 text-red-600" />
      case 'completed': return <CheckCircle className="h-4 w-4 text-blue-600" />
      default: return <Clock className="h-4 w-4 text-yellow-600" />
    }
  }

  const AppointmentCard: React.FC<{ appointment: Appointment }> = ({ appointment }) => (
    <div className="card">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">
              {appointment.patient_name || 'Unknown Patient'}
            </h3>
            {getStatusIcon(appointment.status)}
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <User className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">Dr. {appointment.doctor}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">{formatDate(appointment.scheduled_at)}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">{appointment.procedure}</span>
            </div>
            
            {appointment.notes && (
              <p className="text-sm text-gray-600 mt-2">{appointment.notes}</p>
            )}
          </div>
          
          <div className="flex items-center justify-between mt-4">
            <span className={`status-indicator ${getStatusColor(appointment.status)}`}>
              {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
            </span>
            
            <div className="flex items-center space-x-2">
              <select
                value={appointment.status}
                onChange={(e) => handleStatusChange(appointment.id, e.target.value)}
                className="text-xs border border-gray-300 rounded px-2 py-1"
                disabled={updateMutation.isLoading}
              >
                <option value="pending">Pending</option>
                <option value="confirmed">Confirmed</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
                <option value="no_show">No Show</option>
              </select>
              
              <button
                onClick={() => handleEdit(appointment)}
                className="p-1 text-gray-400 hover:text-healthcare-primary"
              >
                <Edit className="h-4 w-4" />
              </button>
              
              <button
                onClick={() => handleDelete(appointment.id)}
                className="p-1 text-gray-400 hover:text-red-600"
                disabled={deleteMutation.isLoading}
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  const AppointmentForm: React.FC = () => (
    <div className="card mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        {editingAppointment ? 'Edit Appointment' : 'Schedule New Appointment'}
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Patient
            </label>
            <select
              value={formData.patient_id}
              onChange={(e) => setFormData({ ...formData, patient_id: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
              required
            >
              <option value="">Select a patient</option>
              {patients.map((patient) => (
                <option key={patient.id} value={patient.id}>
                  {patient.name || 'Unknown'} ({patient.phone})
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Doctor
            </label>
            <input
              type="text"
              value={formData.doctor}
              onChange={(e) => setFormData({ ...formData, doctor: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
              placeholder="Enter doctor name"
              required
            />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Procedure
            </label>
            <input
              type="text"
              value={formData.procedure}
              onChange={(e) => setFormData({ ...formData, procedure: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
              placeholder="Enter procedure type"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date & Time
            </label>
            <input
              type="datetime-local"
              value={formData.scheduled_at}
              onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
              required
            />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Notes (Optional)
          </label>
          <textarea
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
            rows={3}
            placeholder="Additional notes..."
          />
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            type="submit"
            disabled={createMutation.isLoading || updateMutation.isLoading}
            className="btn-primary"
          >
            {editingAppointment ? 'Update' : 'Schedule'} Appointment
          </button>
          <button
            type="button"
            onClick={() => {
              setShowForm(false)
              setEditingAppointment(null)
              setFormData({
                patient_id: 0,
                doctor: '',
                procedure: '',
                scheduled_at: '',
                notes: ''
              })
            }}
            className="btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )

  if (appointmentsLoading) {
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
            <h1 className="text-2xl font-bold text-gray-900">Appointments</h1>
            <p className="text-gray-600">Manage patient appointments and scheduling</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn-primary"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Appointment
          </button>
        </div>
      </div>

      {/* Form */}
      {showForm && <AppointmentForm />}

      {/* Filters */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search appointments..."
                className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="confirmed">Confirmed</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
              <option value="no_show">No Show</option>
            </select>
          </div>
          
          <div>
            <select
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-healthcare-primary focus:border-transparent"
            >
              <option value="upcoming">Upcoming</option>
              <option value="today">Today</option>
              <option value="past">Past</option>
              <option value="all">All Time</option>
            </select>
          </div>
        </div>
      </div>

      {/* Appointments List */}
      <div className="space-y-4">
        {filteredAppointments.length > 0 ? (
          filteredAppointments.map((appointment) => (
            <AppointmentCard key={appointment.id} appointment={appointment} />
          ))
        ) : (
          <div className="card text-center py-12">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No appointments found</h3>
            <p className="text-gray-600">
              {searchTerm || statusFilter !== 'all' || dateFilter !== 'all'
                ? 'Try adjusting your search or filter criteria'
                : 'Schedule your first appointment to get started'}
            </p>
          </div>
        )}
      </div>

      {/* Statistics */}
      {appointments.length > 0 && (
        <div className="mt-8 grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div className="card text-center">
            <div className="text-2xl font-bold text-healthcare-primary">{appointments.length}</div>
            <div className="text-sm text-gray-600">Total Appointments</div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-green-600">
              {appointments.filter(a => a.status === 'confirmed').length}
            </div>
            <div className="text-sm text-gray-600">Confirmed</div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {appointments.filter(a => a.status === 'pending').length}
            </div>
            <div className="text-sm text-gray-600">Pending</div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-blue-600">
              {appointments.filter(a => a.status === 'completed').length}
            </div>
            <div className="text-sm text-gray-600">Completed</div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Appointments