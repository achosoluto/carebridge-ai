import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Clock, Plus, User } from 'lucide-react';

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
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const [patients, setPatients] = useState<Patient[]>([]);
    const [doctors, setDoctors] = useState<Doctor[]>([]);
    const [showModal, setShowModal] = useState(false);
    const [loading, setLoading] = useState(true);

    const [booking, setBooking] = useState({
        patient: '',
        doctor: '',
        date: '',
        time: ''
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
            alert('Failed to book appointment');
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

    if (loading) return <div className="p-8 text-center text-gray-500">Loading appointments...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-800">Appointments</h1>
                <button
                    onClick={() => setShowModal(true)}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-600 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Book Appointment
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Upcoming Appointments List */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden col-span-2">
                    <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                        <h2 className="font-semibold text-gray-700">Scheduled Appointments</h2>
                    </div>
                    <div className="divide-y divide-gray-100">
                        {appointments.length === 0 ? (
                            <div className="p-8 text-center text-gray-400">No appointments scheduled</div>
                        ) : (
                            appointments.map(appt => (
                                <div key={appt.id} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 rounded-lg bg-blue-50 flex flex-col items-center justify-center text-blue-600 border border-blue-100">
                                            <span className="text-xs font-bold">{new Date(appt.datetime).getDate()}</span>
                                            <span className="text-[10px] uppercase">{new Date(appt.datetime).toLocaleString('default', { month: 'short' })}</span>
                                        </div>
                                        <div>
                                            <h3 className="font-medium text-gray-900">{appt.patient_name}</h3>
                                            <p className="text-sm text-gray-500 flex items-center gap-2">
                                                <User className="w-3 h-3" /> With {appt.doctor_name}
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
                                                {appt.status}
                                            </span>
                                        </div>
                                        {/* Actions could go here */}
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
                        <h2 className="text-xl font-bold mb-4">Book Appointment</h2>
                        <form onSubmit={handleBook}>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Patient</label>
                                    <select
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={booking.patient}
                                        onChange={e => setBooking({ ...booking, patient: e.target.value })}
                                    >
                                        <option value="">Select Patient</option>
                                        {patients.map(p => (
                                            <option key={p.id} value={p.id}>{p.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Doctor</label>
                                    <select
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={booking.doctor}
                                        onChange={e => setBooking({ ...booking, doctor: e.target.value })}
                                    >
                                        <option value="">Select Doctor</option>
                                        {doctors.map(d => (
                                            <option key={d.id} value={d.id}>{d.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                                        <input
                                            required
                                            type="date"
                                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                            value={booking.date}
                                            onChange={e => setBooking({ ...booking, date: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
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
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600"
                                >
                                    Confirm Booking
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Appointments;
