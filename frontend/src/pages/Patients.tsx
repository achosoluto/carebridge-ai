import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Plus, Search, User, Edit } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface Patient {
    id: number;
    name: string;
    language: string;
    contact_info: string;
    created_at: string;
}

const Patients: React.FC = () => {
    const { t } = useTranslation();
    const [patients, setPatients] = useState<Patient[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editingPatient, setEditingPatient] = useState<Patient | null>(null);
    const [newPatient, setNewPatient] = useState({ name: '', language: 'JA', contact_info: '' });
    const [editPatient, setEditPatient] = useState({ id: '', name: '', language: 'JA', contact_info: '' });

    useEffect(() => {
        fetchPatients();
    }, []);

    const fetchPatients = async () => {
        try {
            const response = await api.get('/patients/');
            setPatients(response.data);
        } catch (error) {
            console.error('Error fetching patients:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreatePatient = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/patients/', newPatient);
            setShowModal(false);
            setNewPatient({ name: '', language: 'JA', contact_info: '' });
            fetchPatients(); // Refresh list
        } catch (error) {
            console.error('Error creating patient:', error);
            alert(t('staff.patients.creationFailed'));
        }
    };

    const handleEditPatient = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.put(`/patients/${editPatient.id}/`, {
                name: editPatient.name,
                language: editPatient.language,
                contact_info: editPatient.contact_info
            });
            setShowEditModal(false);
            fetchPatients(); // Refresh list
        } catch (error) {
            console.error('Error updating patient:', error);
            alert('Failed to update patient');
        }
    };

    const handleEditClick = (patient: Patient) => {
        setEditingPatient(patient);
        setEditPatient({
            id: patient.id.toString(),
            name: patient.name,
            language: patient.language,
            contact_info: patient.contact_info
        });
        setShowEditModal(true);
    };

    const filteredPatients = patients.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) return <div className="p-8 text-center text-gray-500">환자 목록 로딩 중...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-800">환자 관리</h1>
                <button
                    onClick={() => setShowModal(true)}
                    className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-600 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    환자 추가
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-4 border-b border-gray-200">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="환자 검색..."
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <table className="w-full text-left">
                    <thead className="bg-gray-50 text-gray-500 text-sm">
                        <tr>
                            <th className="px-6 py-3 font-medium">이름</th>
                            <th className="px-6 py-3 font-medium">언어</th>
                            <th className="px-6 py-3 font-medium">연락처</th>
                            <th className="px-6 py-3 font-medium">등록일</th>
                            <th className="px-6 py-3 font-medium">작업</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {filteredPatients.map((patient) => (
                            <tr key={patient.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600">
                                        <User className="w-4 h-4" />
                                    </div>
                                    <span className="font-medium text-gray-900">{patient.name}</span>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded-full text-xs font-semibold
                    ${patient.language === 'JA' ? 'bg-red-100 text-red-700' :
                                            patient.language === 'ZH' ? 'bg-yellow-100 text-yellow-700' :
                                                'bg-blue-100 text-blue-700'}`}>
                                        {patient.language === 'JA' ? '일본어' :
                                            patient.language === 'ZH' ? '중국어' :
                                                patient.language === 'KO' ? '한국어' : patient.language}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-gray-600">{patient.contact_info || '-'}</td>
                                <td className="px-6 py-4 text-gray-500 text-sm">
                                    {new Date(patient.created_at).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4">
                                    <button
                                        onClick={() => handleEditClick(patient)}
                                        className="text-primary hover:underline text-sm font-medium flex items-center gap-1"
                                    >
                                        <Edit className="w-3 h-3" />
                                        수정
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {filteredPatients.length === 0 && (
                            <tr>
                                <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                                    등록된 환자가 없습니다.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Add Patient Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
                        <h2 className="text-xl font-bold mb-4">환자 추가</h2>
                        <form onSubmit={handleCreatePatient}>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">이름</label>
                                    <input
                                        required
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={newPatient.name}
                                        onChange={e => setNewPatient({ ...newPatient, name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">사용 언어</label>
                                    <select
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={newPatient.language}
                                        onChange={e => setNewPatient({ ...newPatient, language: e.target.value })}
                                    >
                                        <option value="JA">일본어</option>
                                        <option value="ZH">중국어</option>
                                        <option value="KO">한국어</option>
                                        <option value="EN">영어</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">연락처</label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={newPatient.contact_info}
                                        onChange={e => setNewPatient({ ...newPatient, contact_info: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="mt-6 flex justify-end gap-3">
                                <button
                                    type="button"
                                    onClick={() => setShowModal(false)}
                                    className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                                >
                                    취소
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600"
                                >
                                    환자 등록
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Edit Patient Modal */}
            {showEditModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
                        <h2 className="text-xl font-bold mb-4">환자 정보 수정</h2>
                        <form onSubmit={handleEditPatient}>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">이름</label>
                                    <input
                                        required
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={editPatient.name}
                                        onChange={e => setEditPatient({ ...editPatient, name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">사용 언어</label>
                                    <select
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={editPatient.language}
                                        onChange={e => setEditPatient({ ...editPatient, language: e.target.value })}
                                    >
                                        <option value="JA">일본어</option>
                                        <option value="ZH">중국어</option>
                                        <option value="KO">한국어</option>
                                        <option value="EN">영어</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">연락처</label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                                        value={editPatient.contact_info}
                                        onChange={e => setEditPatient({ ...editPatient, contact_info: e.target.value })}
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
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Patients;