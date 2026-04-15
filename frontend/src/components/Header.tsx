import React from 'react';
import { SparklesIcon } from '@heroicons/react/24/outline';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-br from-primary-500 to-secondary-500 p-2 rounded-lg">
            <SparklesIcon className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              AI Landing Page Personalizer
            </h1>
            <p className="text-sm text-gray-600">
              Transform your landing pages with AI
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
