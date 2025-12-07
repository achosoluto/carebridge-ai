import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Calendar, MessageCircle, Info } from 'lucide-react';

const PortalHome: React.FC = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();

    return (
        <div className="max-w-4xl mx-auto">
            <div className="text-center py-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">{t('portal.home.welcome')}</h1>
                <p className="text-xl text-gray-500 mb-8">{t('portal.home.subtitle')}</p>

                <button
                    onClick={() => navigate('/portal/book')}
                    className="bg-primary text-white text-lg px-8 py-3 rounded-full hover:bg-blue-600 transition-shadow shadow-lg shadow-blue-200"
                >
                    {t('portal.home.bookConsultation')}
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
                <div className="p-6 bg-blue-50 rounded-2xl border border-blue-100 text-center">
                    <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <Calendar className="w-6 h-6" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">{t('portal.home.selfBooking')}</h3>
                    <p className="text-gray-500 text-sm">{t('portal.home.selfBookingDesc')}</p>
                </div>
                <div className="p-6 bg-purple-50 rounded-2xl border border-purple-100 text-center">
                    <div className="w-12 h-12 bg-purple-100 text-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <MessageCircle className="w-6 h-6" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">{t('portal.home.support')}</h3>
                    <p className="text-gray-500 text-sm">{t('portal.home.supportDesc')}</p>
                </div>
                <div className="p-6 bg-green-50 rounded-2xl border border-green-100 text-center">
                    <div className="w-12 h-12 bg-green-100 text-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <Info className="w-6 h-6" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">{t('portal.home.procedures')}</h3>
                    <p className="text-gray-500 text-sm">{t('portal.home.proceduresDesc')}</p>
                </div>
            </div>
        </div>
    );
};

export default PortalHome;
