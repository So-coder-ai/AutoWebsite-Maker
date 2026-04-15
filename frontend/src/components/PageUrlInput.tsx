import React, { useState } from 'react';
import { GlobeAltIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { AdAnalysis } from '../App';

interface PageUrlInputProps {
  onSubmit: (url: string) => void;
  loading: boolean;
  adAnalysis: AdAnalysis;
}

const PageUrlInput: React.FC<PageUrlInputProps> = ({ onSubmit, loading, adAnalysis }) => {
  const [url, setUrl] = useState('');
  const [isValid, setIsValid] = useState(false);

  const validateUrl = (input: string) => {
    try {
      new URL(input);
      return true;
    } catch {
      return false;
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUrl(value);
    setIsValid(validateUrl(value));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isValid && url) {
      onSubmit(url);
    }
  };

  return (
    <div className="card">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Step 2: Enter Landing Page URL
        </h2>
        <p className="text-gray-600">
          Provide the URL of the landing page you want to personalize
        </p>
      </div>

      <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-primary-900 mb-3">Ad Analysis Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium text-primary-700">Headline:</span>
            <p className="text-primary-900">{adAnalysis.headline}</p>
          </div>
          <div>
            <span className="font-medium text-primary-700">Tone:</span>
            <p className="text-primary-900">{adAnalysis.tone}</p>
          </div>
          <div>
            <span className="font-medium text-primary-700">Offer:</span>
            <p className="text-primary-900">{adAnalysis.offer}</p>
          </div>
          <div>
            <span className="font-medium text-primary-700">Target Audience:</span>
            <p className="text-primary-900">{adAnalysis.target_audience}</p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="page-url" className="block text-sm font-medium text-gray-700 mb-2">
            Landing Page URL
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <GlobeAltIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="page-url"
              type="url"
              value={url}
              onChange={handleUrlChange}
              placeholder="https://example.com/landing-page"
              className={`input-field pl-10 ${isValid && url ? 'border-green-300 focus:ring-green-500' : ''}`}
              required
            />
            {isValid && url && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-green-500" />
              </div>
            )}
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Enter the complete URL of the landing page you want to enhance
          </p>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={!isValid || !url || loading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Processing<span className="loading-dots"></span></span>
              </span>
            ) : (
              'Generate Personalized Page'
            )}
          </button>
        </div>
      </form>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="font-semibold text-blue-900 mb-2">What happens next?</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• We'll analyze your landing page structure and content</li>
          <li>• AI will enhance the page based on your ad creative</li>
          <li>• You'll see a side-by-side comparison</li>
          <li>• Get a live preview of the personalized version</li>
        </ul>
      </div>
    </div>
  );
};

export default PageUrlInput;
