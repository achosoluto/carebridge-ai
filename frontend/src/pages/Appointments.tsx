import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Clock, Plus, User, Edit, CheckCircle, XCircle, MoreVertical } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface Appointment {
    id: number;
    patient_name: string;
    doctor_name: string;
    datetime: string;
    status: 'PENDING' | 'CONFIRMED' | 'COMPLETED' | 'CANCELLED';
}

interface Doctor {
    id: number;
    name: string;
}

interface Patient {
    id: number;
    name: string;
}

const Appointments: React.FC = () => {
    const { t } = useTranslation();
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const [patients, setPatients] = useState<Patient[]>([]);
    const [doctors, setDoctors] = useState<Doctor[]>([]);
    const [showModal, setShowModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editingAppointment, setEditingAppointment] = useState<Appointment | null>(null);
    const [loading, setLoading] = useState(true);

    const [booking, setBooking] = useState({
        patient: '',
        doctor: '',
        date: '',
        time: ''
    });

    const [editing, setEditing] = useState({
        id: '',
        patient: '',
        doctor: '',
        date: '',
        time: '',
        status: 'PENDING' as 'PENDING' | 'CONFIRMED' | 'COMPLETED' | 'CANCELLED'
    });

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [apptsRes, patientsRes, doctorsRes] = await Promise.all([
                api.get('/appointments/'),
                api.get('/patients/'),
                api.get('/doctors/')
            ]);
            setAppointments(apptsRes.data);
            setPatients(patientsRes.data);
            setDoctors(doctorsRes.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleBook = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const datetime = `${booking.date}T${booking.time}:00Z`; // Simple ISO format
            await api.post('/appointments/', {
                patient: booking.patient,
                doctor: booking.doctor,
                datetime: datetime,
                status: 'CONFIRMED'
            });
            setShowModal(false);
            setBooking({ patient: '', doctor: '', date: '', time: '' });
            fetchData(); // Refresh
        } catch (error) {
            console.error('Error booking appointment:', error);
            alert(t('staff.appointments.bookingFailed'));
        }
    };

    const handleEdit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const datetime = `${editing.date}T${editing.time}:00Z`;
            await api.put(`/appointments/${editing.id}/`, {
                patient: editing.patient,
                doctor: editing.doctor,
                datetime: datetime,
                status: editing.status
            });
            setShowEditModal(false);
            fetchData(); // Refresh
        } catch (error) {
            console.error('Error updating appointment:', error);
            alert('Failed to update appointment');
        }
    };

    const handleEditClick = (appt: Appointment) => {
        setEditingAppointment(appt);
        setEditing({
            id: appt.id.toString(),
            patient: patients.find(p => p.name === appt.patient_name)?.id.toString() || '',
            doctor: doctors.find(d => d.name === appt.doctor_name)?.id.toString() || '',
            date: new Date(appt.datetime).toISOString().split('T')[0],
            time: new Date(appt.datetime).toTimeString().slice(0, 5),
            status: appt.status
        });
        setShowEditModal(true);
    };

    const handleStatusChange = async (appointmentId: number, newStatus: string) => {
        try {
            await api.patch(`/appointments/${appointmentId}/`, { status: newStatus });
            fetchData();
        } catch (error) {
            console.error('Error updating status:', error);
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'CONFIRMED': return 'bg-green-100 text-green-700';
            case 'PENDING': return 'bg-yellow-100 text-yellow-700';
            case 'CANCELLED': return 'bg-red-100 text-red-700';
            case 'COMPLETED': return 'bg-gray-100 text-gray-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    };

    if (loading) return <div className="p-8 text-center text-gray-500">{t('staff.appointments.loadingAppointments')}</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-800">{t('staff.appointments.title')}</h1>
                <button
                    onClick={() => setShowModal(true)}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-600 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    {t('staff.appointments.addAppointment')}
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Upcoming Appointments List */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden col-span-2">
                    <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                        <h2 className="font-semibold text-gray-700">{t('staff.appointments.scheduleTitle')}</h2>
                    </div>
                    <div className="divide-y divide-gray-100">
                        {appointments.length === 0 ? (
                            <div className="p-8 text-center text-gray-400">{t('staff.appointments.noAppointments')}</div>
                        ) : (
                            appointments.map(appt => (
                                <div key={appt.id} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 rounded-lg bg-blue-50 flex flex-col items-center justify-center text-blue-600 border border-blue-100">
                                            <span className="text-xs font-bold">{new Date(appt.datetime).getDate()}</span>
                                            <span className="text-[10px] uppercase">{new Date(appt.datetime).toLocaleString('ko-KR', { month: 'short' })}</span>
                                        </div>
                                        <div>
                                            <h3 className="font-medium text-gray-900">{appt.patient_name}</h3>
                                            <p className="text-sm text-gray-500 flex items-center gap-2">
                                                <User className="w-3 h-3" /> {t('staff.appointments.doctorLabel')}: {appt.doctor_name}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <div className="text-right">
                                            <p className="text-sm font-medium text-gray-900 flex items-center justify-end gap-1">
                                                <Clock className="w-3 h-3 text-gray-400" />
                                                {new Date(appt.datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </p>
                                            <span className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-semibold mt-1 ${getStatusColor(appt.status)}`}>
                                                {t(`staff.appointments.status.${appt.status}`, appt.status)}
                                            </span>
                                        </div>
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() => handleEditClick(appt)}
                                                className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                                                title="Edit appointment"
                                            >
                                                <Edit className="w-4 h-4" />
                                            </button>
                                            <select
                                                value={appt.status}
                                                onChange={(e) => handleStatusChange(appt.id, e.target.value)}
                                                className={`text-xs px-2 py-1 rounded border-0 ${getStatusColor(appt.status)}`}
                                            >
                                                <option value="PENDING">대기</option>
                                                <option value="CONFIRMED">확인</option>
                                                <option value="COMPLETED">완료</option>
                                                <option value="CANCELLED">취소</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>

            {/* Booking Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
                        <h2 className="text-xl font-bold mb-4">{t('staff.appointments.bookAppointment')}</h2>
                        <form onSubmit={handleBook}>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">{t('staff.appointments.selectPatient')}</label>
                                    <select
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={booking.patient}
                                        onChange={e => setBooking({ ...booking, patient: e.target.value })}
                                    >
                                        <option value="">{t('staff.appointments.selectPatientPlaceholder')}</option>
                                        {patients.map(p => (
                                            <option key={p.id} value={p.id}>{p.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">{t('staff.appointments.selectDoctor')}</label>
                                    <select
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={booking.doctor}
                                        onChange={e => setBooking({ ...booking, doctor: e.target.value })}
                                    >
                                        <option value="">{t('staff.appointments.placeholderDoctor')}</option>
                                        {doctors.map(d => (
                                            <option key={d.id} value={d.id}>{d.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">{t('staff.appointments.dateLabel')}</label>
                                        <input
                                            required
                                            type="date"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                            value={booking.date}
                                            onChange={e => setBooking({ ...booking, date: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">{t('staff.appointments.timeLabel')}</label>
                                            <input
                                                required
                                                type="time"
                                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                                value={booking.time}
                                                onChange={e => setBooking({ ...booking, time: e.target.value })}
                                            />
                                        </div>
                                    </div>
                                </div>
                                <div className="mt-6 flex justify-end gap-3">
                                    <button
                                        type="button"
                                        onClick={() => setShowModal(false)}
                                        className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                    >
                                        {t('staff.appointments.cancelButton')}
                                    </button>
                                    <button
                                        type="submit"
                                        className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600"
                                    >
                                        {t('staff.appointments.confirmButton')}
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Edit Modal */}
            {showEditModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
                        <h2 className="text-xl font-bold mb-4">예약 수정</h2>
                        <form onSubmit={handleEdit}>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">환자</label>
                                    <select
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={editing.patient}
                                        onChange={e => setEditing({ ...editing, patient: e.target.value })}
                                    >
                                        {patients.map(p => (
                                            <option key={p.id} value={p.id}>{p.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">의사</label>
                                    <select
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={editing.doctor}
                                        onChange={e => setEditing({ ...editing, doctor: e.target.value })}
                                    >
                                        {doctors.map(d => (
                                            <option key={d.id} value={d.id}>{d.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">상태</label>
                                    <select
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={editing.status}
                                        onChange={e => setEditing({ ...editing, status: e.target.value as any })}
                                    >
                                        <option value="PENDING">대기</option>
                                        <option value="CONFIRMED">확인</option>
                                        <option value="COMPLETED">완료</option>
                                        <option value="CANCELLED">취소</option>
                                    </select>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">날짜</label>
                                        <input
                                            required
                                            type="date"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                            value={editing.date}
                                            onChange={e => setEditing({ ...editing, date: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">시간</label>
                                        <input
                                            required
                                            type="time"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                            value={editing.time}
                                            onChange={e => setEditing({ ...editing, time: e.target.value })}
                                        />
                                    </div>
                                </div>
                                <div className="mt-6 flex justify-end gap-3">
                                    <button
                                        type="button"
                                        onClick={() => setShowEditModal(false)}
                                        className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                    >
                                        취소
                                    </button>
                                    <button
                                        type="submit"
                                        className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600"
                                    >
                                        수정
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Appointments;