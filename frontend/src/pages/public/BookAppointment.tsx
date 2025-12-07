import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Calendar, User, Phone, Globe, CheckCircle } from 'lucide-react';

const BookAppointment: React.FC = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const [doctors, setDoctors] = useState<any[]>([]);
    const [formData, setFormData] = useState({
        doctor: '',
        date: '',
        time: '',
        patient_name: '',
        patient_contact: '',
        patient_language: 'JA'
    });
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        api.get('/public/doctors/')
            .then(res => setDoctors(res.data))
            .catch(err => console.error("Failed to fetch doctors", err));
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const datetime = `${formData.date}T${formData.time}`;
            await api.post('/public/appointments/', {
                doctor: formData.doctor,
                datetime: datetime,
                patient_name: formData.patient_name,
                patient_contact: formData.patient_contact,
                patient_language: formData.patient_language
            });
            setSubmitted(true);
        } catch (error) {
            console.error("Booking failed", error);
            alert("Failed to book appointment. Please try again.");
        }
    };

    if (submitted) {
        return (
            <div className="max-w-md mx-auto py-12 text-center">
                <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                    <CheckCircle className="w-10 h-10" />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">{t('portal.bookAppointment.bookingConfirmed')}</h2>
                <p className="text-gray-500 mb-8">{t('portal.bookAppointment.confirmationMessage')}</p>
                <button
                    onClick={() => navigate('/portal')}
                    className="bg-primary text-white px-8 py-3 rounded-full hover:bg-blue-600"
                >
                    {t('portal.bookAppointment.backToHome')}
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">{t('portal.bookAppointment.title')}</h1>

            <form onSubmit={handleSubmit} className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">

                {/* Doctor Selection */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                        <User className="w-4 h-4" /> {t('portal.bookAppointment.selectDoctor')}
                    </label>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {doctors.map(doc => (
                            <div
                                key={doc.id}
                                onClick={() => setFormData({ ...formData, doctor: doc.id })}
                                className={`p-4 rounded-xl border cursor-pointer transition-all ${formData.doctor === doc.id
                                    ? 'border-primary bg-primary/5 ring-2 ring-primary/20'
                                    : 'border-gray-200 hover:border-primary/50'
                                    }`}
                            >
                                <div className="font-medium text-gray-900">Dr. {doc.name}</div>
                                <div className="text-sm text-gray-500">{doc.specialty}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Date & Time */}
                <div className="grid grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                            <Calendar className="w-4 h-4" /> {t('portal.bookAppointment.date')}
                        </label>
                        <input
                            required
                            type="date"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
                            value={formData.date}
                            onChange={e => setFormData({ ...formData, date: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                            <Calendar className="w-4 h-4" /> {t('portal.bookAppointment.time')}
                        </label>
                        <input
                            required
                            type="time"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
                            value={formData.time}
                            onChange={e => setFormData({ ...formData, time: e.target.value })}
                        />
                    </div>
                </div>

                {/* Patient Details */}
                <div className="space-y-4 pt-4 border-t border-gray-100">
                    <h3 className="font-medium text-gray-900">{t('portal.bookAppointment.yourDetails')}</h3>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">{t('portal.bookAppointment.fullName')}</label>
                        <input
                            required
                            type="text"
                            placeholder="예: 홍길동"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
                            value={formData.patient_name}
                            onChange={e => setFormData({ ...formData, patient_name: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-2">
                            <Phone className="w-4 h-4" /> {t('portal.bookAppointment.contact')}
                        </label>
                        <input
                            required
                            type="text"
                            placeholder="예약 확인을 위한 연락처 정보"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
                            value={formData.patient_contact}
                            onChange={e => setFormData({ ...formData, patient_contact: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-2">
                            <Globe className="w-4 h-4" /> {t('portal.bookAppointment.preferredLanguage')}
                        </label>
                        <select
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:outline-none"
                            value={formData.patient_language}
                            onChange={e => setFormData({ ...formData, patient_language: e.target.value })}
                        >
                            <option value="JA">일본어</option>
                            <option value="ZH">중국어</option>
                            <option value="KO">한국어</option>
                            <option value="EN">영어</option>
                        </select>
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={!formData.doctor || !formData.date || !formData.time}
                    className="w-full bg-primary text-white py-3 rounded-xl font-bold text-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {t('portal.bookAppointment.confirmBooking')}
                </button>
            </form>
        </div>
    );
};

export default BookAppointment;
