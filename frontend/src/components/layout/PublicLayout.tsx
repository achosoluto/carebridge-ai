import React from 'react';
import { Outlet } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import i18n from '../../i18n';
import ChatWidget from '../ChatWidget';

const PublicLayout: React.FC = () => {
    const { t } = useTranslation();

    const handleLanguageChange = (language: string) => {
        i18n.changeLanguage(language);
        localStorage.setItem('language', language);
    };

    return (
        <div className="min-h-screen bg-white">
            <header className="border-b border-gray-100 py-4">
                <div className="container mx-auto px-4 flex justify-between items-center">
                    <h1 className="text-xl font-bold text-primary">{t('portal.layout.title')}</h1>
                    <div className="flex items-center gap-6">
                        <nav className="text-sm text-gray-600 gap-4 flex">
                            <a href="/portal" className="hover:text-primary">{t('portal.layout.home')}</a>
                            <a href="/portal/book" className="hover:text-primary">{t('portal.layout.bookNow')}</a>
                        </nav>
                        <select
                            className="text-sm border border-gray-200 rounded px-2 py-1 text-gray-600 focus:outline-none focus:border-primary"
                            value={i18n.language}
                            onChange={(e) => handleLanguageChange(e.target.value)}
                        >
                            <option value="en">English</option>
                            <option value="ko">한국어</option>
                            <option value="ja">日本語</option>
                            <option value="zh">中文</option>
                        </select>
                    </div>
                </div>
            </header>
            <main className="container mx-auto px-4 py-8">
                <Outlet />
            </main>
            <footer className="bg-gray-50 py-8 mt-12 bg-white">
                <div className="container mx-auto px-4 text-center text-gray-400 text-sm">
                    {t('portal.layout.copyright')}
                </div>
            </footer>
            <ChatWidget />
        </div>
    );
};

export default PublicLayout;
