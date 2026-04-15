import { useState } from 'react';
import { toast } from 'react-toastify';
import { api } from '../utils/api';

export const usePagePersonalization = () => {
  const [loading, setLoading] = useState(false);

  const analyzeAd = async (input: {
    file?: File;
    adUrl?: string;
    adText?: string;
  }) => {
    setLoading(true);
    try {
      const formData = new FormData();
      
      if (input.file) {
        formData.append('file', input.file);
      } else if (input.adUrl) {
        formData.append('ad_url', input.adUrl);
      } else if (input.adText) {
        formData.append('ad_text', input.adText);
      }

      const result = await api.analyzeAd(formData);
      return result.analysis;
    } catch (error) {
      console.error('Error analyzing ad:', error);
      toast.error('Failed to analyze ad creative');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const scrapePage = async (url: string) => {
    setLoading(true);
    try {
      const result = await api.scrapePage(url);
      return result.content;
    } catch (error) {
      console.error('Error scraping page:', error);
      toast.error('Failed to analyze landing page');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const generatePersonalizedPage = async (data: {
    ad_analysis: any;
    page_content: any;
    page_url: string;
  }) => {
    setLoading(true);
    try {
      const result = await api.generatePersonalizedPage(data);
      return result;
    } catch (error) {
      console.error('Error generating personalized page:', error);
      toast.error('Failed to generate personalized page');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return {
    analyzeAd,
    scrapePage,
    generatePersonalizedPage,
    loading,
  };
};
