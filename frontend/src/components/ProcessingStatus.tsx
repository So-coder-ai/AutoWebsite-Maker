import React, { useState, useEffect } from 'react';
import {
  SparklesIcon,
  CpuChipIcon,
  DocumentTextIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

interface ProcessingStatusProps {
  isVisible: boolean;
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ isVisible }) => {
  const [currentStep, setCurrentStep] = useState(0);
  
  const steps = [
    { icon: SparklesIcon, title: 'Analyzing Ad Creative', description: 'Extracting key information from your ad' },
    { icon: CpuChipIcon, title: 'Scraping Landing Page', description: 'Analyzing page structure and content' },
    { icon: DocumentTextIcon, title: 'Generating Personalization', description: 'Creating AI-powered enhancements' },
    { icon: CheckCircleIcon, title: 'Finalizing Results', description: 'Preparing your personalized page' }
  ];
  
  useEffect(() => {
    if (!isVisible) {
      setCurrentStep(0);
      return;
    }
    
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 3000);
    
    return () => clearInterval(interval);
  }, [isVisible, steps.length]);
  
  if (!isVisible) return null;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
          <SparklesIcon className="h-8 w-8 text-primary-600 animate-pulse" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Creating Your Personalized Page
        </h2>
        <p className="text-lg text-gray-600">
          Our AI is analyzing your ad creative and enhancing your landing page
        </p>
      </div>

      <div className="card">
        <div className="space-y-6">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = index === currentStep;
            const isCompleted = index < currentStep;

            return (
              <div
                key={index}
                className={`flex items-center space-x-4 p-4 rounded-lg transition-all duration-300 ${
                  isActive
                    ? 'bg-primary-50 border-2 border-primary-200'
                    : isCompleted
                    ? 'bg-green-50 border-2 border-green-200'
                    : 'bg-gray-50 border-2 border-transparent'
                }`}
              >
                <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${
                  isActive
                    ? 'bg-primary-600 text-white'
                    : isCompleted
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                }`}>
                  {isCompleted ? (
                    <CheckCircleIcon className="h-6 w-6" />
                  ) : (
                    <Icon className={`h-6 w-6 ${isActive ? 'animate-pulse' : ''}`} />
                  )}
                </div>
                
                <div className="flex-1">
                  <h3 className={`font-semibold ${
                    isActive
                      ? 'text-primary-900'
                      : isCompleted
                      ? 'text-green-900'
                      : 'text-gray-600'
                  }`}>
                    {step.label}
                  </h3>
                  <p className={`text-sm ${
                    isActive
                      ? 'text-primary-700'
                      : isCompleted
                      ? 'text-green-700'
                      : 'text-gray-500'
                  }`}>
                    {step.description}
                  </p>
                </div>

                {isActive && (
                  <div className="flex-shrink-0">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">What's happening?</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Extracting key elements from your landing page</li>
            <li>• Analyzing ad creative for messaging insights</li>
            <li>• Applying conversion rate optimization principles</li>
            <li>• Maintaining your original design while enhancing content</li>
          </ul>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            This usually takes 30-60 seconds. Please don't close this window.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus;
