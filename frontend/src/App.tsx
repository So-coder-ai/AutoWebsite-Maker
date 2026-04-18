import React, { useState } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './components/Header';
import AdInput from './components/AdInput';
import PageUrlInput from './components/PageUrlInput';
import ProcessingStatus from './components/ProcessingStatus';
import ResultsDisplay from './components/ResultsDisplay';
import { usePagePersonalization } from './hooks/usePagePersonalization';

export interface AdAnalysis {
  headline: string;
  tone: string;
  offer: string;
  target_audience: string;
  brand_voice: string;
  cta?: string;
}

export interface PageContent {
  url: string;
  title: string;
  structure: any;
  content: any;
  components: any;
}

export interface PersonalizedResult {
  id: string;
  original_url: string;
  personalized_url: string;
  created_at: string;
  ad_analysis: AdAnalysis;
  changes_summary: string;
}

function App() {
  const [step, setStep] = useState<'input' | 'processing' | 'results'>('input');
  const [adData, setAdData] = useState<AdAnalysis | null>(null);
  const [result, setResult] = useState<PersonalizedResult | null>(null);

  const { scrapePage, generatePersonalizedPage, loading } = usePagePersonalization();

  const handleAdSubmit = async (data: AdAnalysis) => {
    setAdData(data);
  };

  const handlePageSubmit = async (url: string) => {
    if (!adData) {
      return;
    }

    setStep('processing');
    
    try {
      const pageContent = await scrapePage(url);

      const personalizedResult = await generatePersonalizedPage({
        ad_analysis: adData,
        page_content: pageContent,
        page_url: url
      });

      setResult(personalizedResult);
      setStep('results');
    } catch (error) {
      console.error('Error processing:', error);
      setStep('input');
    }
  };

  const handleReset = () => {
    setStep('input');
    setAdData(null);
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {step === 'input' && (
          <div className="max-w-4xl mx-auto space-y-8">
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Project Humanise
              </h1>
              <p className="text-xl text-gray-600">
                Personalize existing landing pages using ad-aligned messaging
              </p>
            </div>

            <AdInput 
              onAnalyze={handleAdSubmit}
              loading={loading}
            />
            
            {adData && (
              <PageUrlInput 
                onSubmit={handlePageSubmit}
                loading={loading}
                adAnalysis={adData}
              />
            )}
          </div>
        )}

        {step === 'processing' && (
          <ProcessingStatus isVisible />
        )}

        {step === 'results' && result && (
          <ResultsDisplay 
            result={result}
            onReset={handleReset}
          />
        )}
      </main>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
}

export default App;
