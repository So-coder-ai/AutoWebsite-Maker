import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import { CloudArrowUpIcon, LinkIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import { AdAnalysis } from '../App';

interface AdInputProps {
  onAnalyze: (analysis: AdAnalysis) => void;
  loading: boolean;
}

const AdInput: React.FC<AdInputProps> = ({ onAnalyze, loading }) => {
  const [inputMethod, setInputMethod] = useState<'file' | 'url' | 'text'>('file');
  const [file, setFile] = useState<File | null>(null);
  const [adUrl, setAdUrl] = useState('');
  const [adText, setAdText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    },
  });

  const handleAnalyze = async () => {
    setAnalyzing(true);
    
    try {
      const formData = new FormData();
      
      if (inputMethod === 'file' && file) {
        formData.append('file', file);
      } else if (inputMethod === 'url' && adUrl) {
        formData.append('ad_url', adUrl);
      } else if (inputMethod === 'text' && adText) {
        formData.append('ad_text', adText);
      } else {
        toast.error('Please provide ad creative input');
        setAnalyzing(false);
        return;
      }

      const response = await fetch('/analyze-ad', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const result = await response.json();
      onAnalyze(result.analysis);
      toast.success('Ad creative analyzed successfully!');
      
    } catch (error) {
      console.error('Error analyzing ad:', error);
      toast.error('Failed to analyze ad creative. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="card">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Step 1: Upload Ad Creative
        </h2>
        <p className="text-gray-600">
          Provide your ad creative for AI analysis
        </p>
      </div>

      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setInputMethod('file')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            inputMethod === 'file'
              ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
              : 'bg-gray-100 text-gray-700 border-2 border-transparent'
          }`}
        >
          <CloudArrowUpIcon className="h-5 w-5" />
          <span>Upload File</span>
        </button>
        
        <button
          onClick={() => setInputMethod('url')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            inputMethod === 'url'
              ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
              : 'bg-gray-100 text-gray-700 border-2 border-transparent'
          }`}
        >
          <LinkIcon className="h-5 w-5" />
          <span>Ad URL</span>
        </button>
        
        <button
          onClick={() => setInputMethod('text')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            inputMethod === 'text'
              ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
              : 'bg-gray-100 text-gray-700 border-2 border-transparent'
          }`}
        >
          <DocumentTextIcon className="h-5 w-5" />
          <span>Ad Text</span>
        </button>
      </div>

      {inputMethod === 'file' && (
        <div className="mb-6">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-400 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            {file ? (
              <div>
                <p className="text-lg font-medium text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-600">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            ) : (
              <div>
                <p className="text-lg font-medium text-gray-900 mb-2">
                  {isDragActive ? 'Drop your ad creative here' : 'Drag & drop your ad creative'}
                </p>
                <p className="text-sm text-gray-600">
                  or click to browse (PNG, JPG, GIF, WebP)
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {inputMethod === 'url' && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ad Creative URL
          </label>
          <input
            type="url"
            value={adUrl}
            onChange={(e) => setAdUrl(e.target.value)}
            placeholder="https://example.com/ad-creative"
            className="input-field"
          />
          <p className="text-sm text-gray-600 mt-2">
            Enter the URL where your ad creative is hosted
          </p>
        </div>
      )}

      {inputMethod === 'text' && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ad Copy Text
          </label>
          <textarea
            value={adText}
            onChange={(e) => setAdText(e.target.value)}
            placeholder="Enter your ad copy text here..."
            rows={6}
            className="input-field resize-none"
          />
          <p className="text-sm text-gray-600 mt-2">
            Paste your ad copy text for analysis
          </p>
        </div>
      )}

      <div className="flex justify-end">
        <button
          onClick={handleAnalyze}
          disabled={analyzing || loading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {analyzing ? (
            <span className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Analyzing<span className="loading-dots"></span></span>
            </span>
          ) : (
            'Analyze Ad Creative'
          )}
        </button>
      </div>
    </div>
  );
};

export default AdInput;
