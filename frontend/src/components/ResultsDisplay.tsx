import React, { useState } from 'react';
import { 
  ArrowTopRightOnSquareIcon, 
  ArrowLeftIcon, 
  EyeIcon,
  DocumentDuplicateIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { PersonalizedResult } from '../App';

interface ResultsDisplayProps {
  result: PersonalizedResult;
  onReset: () => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result, onReset }) => {
  const [viewMode, setViewMode] = useState<'split' | 'original' | 'personalized'>('split');
  const [copied, setCopied] = useState(false);

  const handleCopyUrl = async () => {
    try {
      const fullUrl = `${window.location.origin}${result.personalized_url}`;
      await navigator.clipboard.writeText(fullUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy URL:', error);
    }
  };

  const openPersonalizedPage = () => {
    window.open(result.personalized_url, '_blank');
  };

  const openOriginalPage = () => {
    window.open(result.original_url, '_blank');
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
          <SparklesIcon className="h-8 w-8 text-green-600" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Your Personalized Landing Page is Ready!
        </h2>
        <p className="text-lg text-gray-600">
          AI has enhanced your landing page based on your ad creative
        </p>
      </div>

      <div className="flex flex-wrap justify-center gap-4 mb-8">
        <button
          onClick={openPersonalizedPage}
          className="btn-primary flex items-center space-x-2"
        >
          <ArrowTopRightOnSquareIcon className="h-5 w-5" />
          <span>View Personalized Page</span>
        </button>
        
        <button
          onClick={handleCopyUrl}
          className="btn-secondary flex items-center space-x-2"
        >
          <DocumentDuplicateIcon className="h-5 w-5" />
          <span>{copied ? 'URL Copied!' : 'Copy URL'}</span>
        </button>
        
        <button
          onClick={openOriginalPage}
          className="btn-secondary flex items-center space-x-2"
        >
          <EyeIcon className="h-5 w-5" />
          <span>View Original</span>
        </button>
        
        <button
          onClick={onReset}
          className="btn-secondary flex items-center space-x-2"
        >
          <ArrowLeftIcon className="h-5 w-5" />
          <span>Create New</span>
        </button>
      </div>

      <div className="flex justify-center mb-6">
        <div className="inline-flex rounded-lg border border-gray-200 bg-white p-1">
          <button
            onClick={() => setViewMode('split')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              viewMode === 'split'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Side by Side
          </button>
          <button
            onClick={() => setViewMode('original')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              viewMode === 'original'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Original
          </button>
          <button
            onClick={() => setViewMode('personalized')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              viewMode === 'personalized'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Personalized
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {(viewMode === 'split' || viewMode === 'original') && (
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Original Page</h3>
              <span className="text-sm text-gray-500">{result.original_url}</span>
            </div>
            <div className="border border-gray-200 rounded-lg overflow-hidden" style={{ height: '600px' }}>
              <iframe
                src={result.original_url}
                className="w-full h-full"
                title="Original Page"
                sandbox="allow-same-origin allow-scripts allow-forms"
              />
            </div>
          </div>
        )}

        {(viewMode === 'split' || viewMode === 'personalized') && (
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-green-700">Personalized Page</h3>
              <span className="text-sm text-green-600">AI Enhanced</span>
            </div>
            <div className="border border-green-200 rounded-lg overflow-hidden" style={{ height: '600px' }}>
              <iframe
                src={result.personalized_url}
                className="w-full h-full"
                title="Personalized Page"
                sandbox="allow-same-origin allow-scripts allow-forms"
              />
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 card">
        <h3 className="text-xl font-bold text-gray-900 mb-4">AI Enhancement Summary</h3>
        <div className="prose max-w-none">
          <p className="text-gray-700">{result.changes_summary}</p>
        </div>
        
        <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
          <h4 className="font-semibold text-primary-900 mb-3">Based on Your Ad Analysis:</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-primary-700">Headline:</span>
              <p className="text-primary-900">{result.ad_analysis.headline}</p>
            </div>
            <div>
              <span className="font-medium text-primary-700">Tone:</span>
              <p className="text-primary-900">{result.ad_analysis.tone}</p>
            </div>
            <div>
              <span className="font-medium text-primary-700">Target Audience:</span>
              <p className="text-primary-900">{result.ad_analysis.target_audience}</p>
            </div>
            <div>
              <span className="font-medium text-primary-700">Offer:</span>
              <p className="text-primary-900">{result.ad_analysis.offer}</p>
            </div>
          </div>
        </div>

        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h4 className="font-semibold text-green-900 mb-3">Next Steps:</h4>
          <ul className="text-sm text-green-800 space-y-1">
            <li>• Test the personalized page with A/B testing</li>
            <li>• Monitor conversion rates and user engagement</li>
            <li>• Share the enhanced page with your team</li>
            <li>• Create variations for different ad campaigns</li>
          </ul>
        </div>
      </div>

      <div className="mt-8 text-center">
        <p className="text-gray-600 mb-4">
          Share your personalized landing page with your team
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={handleCopyUrl}
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Copy Link
          </button>
          <span className="text-gray-400">•</span>
          <button
            onClick={openPersonalizedPage}
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Open in New Tab
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
