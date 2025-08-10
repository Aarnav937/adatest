import React, { useState, useRef } from 'react';
import './DocumentAnalysisWidget.css';

const DocumentAnalysisWidget = ({ documentData, onClose }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Convert file to base64
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64Data = e.target.result.split(',')[1]; // Remove data URL prefix
        
        // Emit document analysis request
        if (window.socket) {
          window.socket.emit('document_analysis_request', {
            file_data: base64Data,
            filename: file.name,
            analysis_type: 'extract' // Default to extract, can be changed
          });
        }
        
        setUploadProgress(100);
        setIsUploading(false);
      };
      
      reader.readAsDataURL(file);
      
      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 100);
      
    } catch (error) {
      console.error('File upload error:', error);
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleAnalysisTypeChange = (analysisType) => {
    if (documentData && window.socket) {
      window.socket.emit('document_analysis_request', {
        document_id: documentData.document_id,
        analysis_type: analysisType
      });
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="document-analysis-widget">
      <div className="widget-header">
        <h3>📄 Document Analysis</h3>
        <button className="close-button" onClick={onClose}>×</button>
      </div>

      <div className="widget-content">
        {!documentData ? (
          <div className="upload-section">
            <div className="upload-area" onClick={() => fileInputRef.current?.click()}>
              <div className="upload-icon">📁</div>
              <p>Click to upload a document</p>
              <p className="supported-formats">
                Supported: PDF, DOCX, TXT, MD, RTF, CSV, XLSX, PPTX, PNG, JPG
              </p>
            </div>
            
            {isUploading && (
              <div className="upload-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
                <p>Uploading... {uploadProgress}%</p>
              </div>
            )}
            
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt,.md,.rtf,.csv,.xlsx,.pptx,.png,.jpg,.jpeg"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
          </div>
        ) : (
          <div className="analysis-section">
            <div className="document-info">
              <h4>📋 Document Information</h4>
              <p><strong>Filename:</strong> {documentData.filename}</p>
              <p><strong>Content Length:</strong> {documentData.content_length} characters</p>
              <p><strong>Analysis Type:</strong> {documentData.analysis_type}</p>
            </div>

            <div className="analysis-controls">
              <h4>🔍 Analysis Options</h4>
              <div className="analysis-buttons">
                <button 
                  onClick={() => handleAnalysisTypeChange('extract')}
                  className={documentData.analysis_type === 'extract' ? 'active' : ''}
                >
                  Extract Content
                </button>
                <button 
                  onClick={() => handleAnalysisTypeChange('summarize')}
                  className={documentData.analysis_type === 'summarize' ? 'active' : ''}
                >
                  Summarize
                </button>
                <button 
                  onClick={() => handleAnalysisTypeChange('qa')}
                  className={documentData.analysis_type === 'qa' ? 'active' : ''}
                >
                  Q&A
                </button>
              </div>
            </div>

            <div className="analysis-results">
              <h4>📊 Analysis Results</h4>
              
              {documentData.extracted_content && (
                <div className="result-section">
                  <h5>Extracted Content</h5>
                  <div className="content-preview">
                    {documentData.extracted_content.length > 500 
                      ? documentData.extracted_content.substring(0, 500) + '...'
                      : documentData.extracted_content
                    }
                  </div>
                </div>
              )}

              {documentData.summary && (
                <div className="result-section">
                  <h5>Summary</h5>
                  <div className="summary-text">
                    {documentData.summary}
                  </div>
                </div>
              )}

              {documentData.question && documentData.answer && (
                <div className="result-section">
                  <h5>Q&A</h5>
                  <div className="qa-item">
                    <p><strong>Question:</strong> {documentData.question}</p>
                    <p><strong>Answer:</strong> {documentData.answer}</p>
                  </div>
                </div>
              )}
            </div>

            <div className="document-actions">
              <button className="action-button" onClick={() => fileInputRef.current?.click()}>
                📁 Upload New Document
              </button>
              <button className="action-button delete" onClick={() => {
                if (window.socket) {
                  window.socket.emit('delete_document_request', {
                    document_id: documentData.document_id
                  });
                }
              }}>
                🗑️ Delete Document
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentAnalysisWidget;
