import { useState } from 'react'
import { useAppointments, usePatients, useCreateAppointment, useUpdateAppointment, useDeleteAppointment } from '../hooks/useApi'
import { Calendar, Clock, User, Plus, Search, Filter, Edit2, Trash2, CheckCircle, XCircle } from 'lucide-react'
import type { Appointment, AppointmentFormData } from '../types'

export default function Appointments() {
    const [showForm, setShowForm] = useState(false)
    const [editingAppointment, setEditingAppointment] = useState<Appointment | null>(null)
    const [searchTerm, setSearchTerm] = useState('')
    const [statusFilter, setStatusFilter] = useState<string>('all')

    const { data: appointments = [], isLoading } = useAppointments()
    const { data: patients = [] } = usePatients()
    const createMutation = useCreateAppointment()
    const updateMutation = useUpdateAppointment()
    const deleteMutation = useDeleteAppointment()

    const [formData, setFormData] = useState<AppointmentFormData>({
        patient_id: 0,
        doctor: '',
        procedure: '',
        scheduled_at: '',
        notes: ''
    })

    const filteredAppointments = appointments.filter(apt => {
        const matchesSearch = apt.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            apt.doctor.toLowerCase().includes(searchTerm.toLowerCase())
        const matchesStatus = statusFilter === 'all' || apt.status === statusFilter
        return matchesSearch && matchesStatus
    })

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()

        if (editingAppointment) {
            updateMutation.mutate({ id: editingAppointment.id, data: formData })
        } else {
            createMutation.mutate(formData)
        }

        setShowForm(false)
        setEditingAppointment(null)
        setFormData({ patient_id: 0, doctor: '', procedure: '', scheduled_at: '', notes: '' })
    }

    const handleEdit = (appointment: Appointment) => {
        setEditingAppointment(appointment)
        setFormData({
            patient_id: appointment.patient,
            doctor: appointment.doctor,
            procedure: appointment.procedure,
            scheduled_at: appointment.scheduled_at,
            notes: appointment.notes || ''
        })
        setShowForm(true)
    }

    const handleDelete = (id: number) => {
        if (confirm('Are you sure you want to delete this appointment?')) {
            deleteMutation.mutate(id)
        }
    }

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'confirmed': return 'bg-green-100 text-green-700'
            case 'pending': return 'bg-yellow-100 text-yellow-700'
            case 'completed': return 'bg-blue-100 text-blue-700'
            case 'cancelled': return 'bg-red-100 text-red-700'
            default: return 'bg-gray-100 text-gray-700'
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-900 mb-2">Appointments</h1>
                        <p className="text-gray-600">Manage patient appointments and scheduling</p>
                    </div>
                    <button
                        onClick={() => {
                            setShowForm(true)
                            setEditingAppointment(null)
                            setFormData({ patient_id: 0, doctor: '', procedure: '', scheduled_at: '', notes: '' })
                        }}
                        className="flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors shadow-lg"
                    >
                        <Plus className="w-5 h-5" />
                        New Appointment
                    </button>
                </div>

                {/* Filters */}
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search by patient or doctor..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div className="relative">
                            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none"
                            >
                                <option value="all">All Statuses</option>
                                <option value="pending">Pending</option>
                                <option value="confirmed">Confirmed</option>
                                <option value="completed">Completed</option>
                                <option value="cancelled">Cancelled</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Appointments List */}
                <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                    {isLoading ? (
                        <div className="text-center py-12">
                            <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
                            <p className="text-gray-500 mt-4">Loading appointments...</p>
                        </div>
                    ) : filteredAppointments.length === 0 ? (
                        <div className="text-center py-12">
                            <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <p className="text-gray-500">No appointments found</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {filteredAppointments.map((appointment) => (
                                <div key={appointment.id} className="p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-3 mb-2">
                                                <User className="w-5 h-5 text-gray-400" />
                                                <span className="font-semibold text-gray-900">{appointment.patient_name}</span>
                                                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(appointment.status)}`}>
                                                    {appointment.status}
                                                </span>
                                            </div>
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm text-gray-600 ml-8">
                                                <div className="flex items-center gap-2">
                                                    <User className="w-4 h-4" />
                                                    Dr. {appointment.doctor}
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <Clock className="w-4 h-4" />
                                                    {new Date(appointment.scheduled_at).toLocaleString()}
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <Calendar className="w-4 h-4" />
                                                    {appointment.procedure}
                                                </div>
                                            </div>
                                            {appointment.notes && (
                                                <p className="text-sm text-gray-500 mt-2 ml-8">{appointment.notes}</p>
                                            )}
                                        </div>
                                        <div className="flex items-center gap-2 ml-4">
                                            <button
                                                onClick={() => handleEdit(appointment)}
                                                className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                            >
                                                <Edit2 className="w-4 h-4" />
                                            </button>
                                            <button
                                                onClick={() => handleDelete(appointment.id)}
                                                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Create/Edit Form Modal */}
                {showForm && (
                    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setShowForm(false)}>
                        <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
                            <div className="p-6 border-b border-gray-200">
                                <h2 className="text-2xl font-bold text-gray-900">
                                    {editingAppointment ? 'Edit Appointment' : 'New Appointment'}
                                </h2>
                            </div>
                            <form onSubmit={handleSubmit} className="p-6 space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Patient</label>
                                    <select
                                        value={formData.patient_id}
                                        onChange={(e) => setFormData({ ...formData, patient_id: parseInt(e.target.value) })}
                                        className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    >
                                        <option value={0}>Select a patient</option>
                                        {patients.map((patient) => (
                                            <option key={patient.id} value={patient.id}>
                                                {patient.name} ({patient.phone})
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">Doctor</label>
                                        <input
                                            type="text"
                                            value={formData.doctor}
                                            onChange={(e) => setFormData({ ...formData, doctor: e.target.value })}
                                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            placeholder="Dr. Smith"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">Procedure</label>
                                        <input
                                            type="text"
                                            value={formData.procedure}
                                            onChange={(e) => setFormData({ ...formData, procedure: e.target.value })}
                                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            placeholder="Checkup"
                                            required
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Scheduled Date & Time</label>
                                    <input
                                        type="datetime-local"
                                        value={formData.scheduled_at}
                                        onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Notes (Optional)</label>
                                    <textarea
                                        value={formData.notes}
                                        onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        rows={3}
                                        placeholder="Additional notes..."
                                    />
                                </div>

                                <div className="flex gap-3 pt-4">
                                    <button
                                        type="submit"
                                        disabled={createMutation.isLoading || updateMutation.isLoading}
                                        className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors disabled:bg-gray-300"
                                    >
                                        <CheckCircle className="w-5 h-5" />
                                        {editingAppointment ? 'Update' : 'Create'} Appointment
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setShowForm(false)}
                                        className="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors"
                                    >
                                        <XCircle className="w-5 h-5" />
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
