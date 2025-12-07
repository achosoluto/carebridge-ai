import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Users, Calendar, MessageSquare } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const Dashboard: React.FC = () => {
    const { t } = useTranslation();
    const [stats, setStats] = useState({
        patients: 0,
        appointments: 0,
        messages: 0
    });

    useEffect(() => {
        // In a real app, fetch dashboard stats. For now, we mock or fetch counts.
        // Let's just create placeholder stats
        const fetchStats = async () => {
            try {
                // Parallel fetch for simple counts
                const [patientsRes, apptsRes, msgsRes] = await Promise.all([
                    api.get('/patients/'),
                    api.get('/appointments/'),
                    api.get('/messages/')
                ]);
                setStats({
                    patients: patientsRes.data.length,
                    appointments: apptsRes.data.length,
                    messages: msgsRes.data.length
                });
            } catch (error) {
                console.error("Failed to fetch stats", error);
            }
        };
        fetchStats();
    }, []);

    const StatCard = ({ title, count, icon: Icon, color }: any) => (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm text-gray-500 mb-1">{title}</p>
                    <h3 className="text-3xl font-bold text-gray-800">{count}</h3>
                </div>
                <div className={`p-3 rounded-full ${color}`}>
                    <Icon className="w-6 h-6 text-white" />
                </div>
            </div>
        </div>
    );

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatCard title={t('staff.dashboard.totalPatients')} count={stats.patients} icon={Users} color="bg-blue-500" />
                <StatCard title={t('staff.dashboard.todaysAppointments')} count={stats.appointments} icon={Calendar} color="bg-green-500" />
                <StatCard title={t('staff.dashboard.unreadMessages')} count={stats.messages} icon={MessageSquare} color="bg-purple-500" />
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">{t('staff.dashboard.recentActivity')}</h3>
                <p className="text-gray-500">{t('staff.dashboard.noRecentActivity')}</p>
            </div>
        </div>
    );
};

export default Dashboard;
