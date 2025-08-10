import React, { useState } from 'react';
import './ImageGenerationWidget.css';

const ImageGenerationWidget = ({ imageData, onClose }) => {
  const [prompt, setPrompt] = useState('');
  const [negativePrompt, setNegativePrompt] = useState('');
  const [width, setWidth] = useState(1024);
  const [height, setHeight] = useState(1024);
  const [steps, setSteps] = useState(20);
  const [guidance, setGuidance] = useState(7.5);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);

  const handleGenerateImage = () => {
    if (!prompt.trim()) return;

    setIsGenerating(true);
    setGenerationProgress(0);

    // Emit image generation request
    if (window.socket) {
      window.socket.emit('image_generation_request', {
        prompt: prompt.trim(),
        negative_prompt: negativePrompt.trim(),
        width: width,
        height: height,
        num_inference_steps: steps,
        guidance_scale: guidance
      });
    }

    // Simulate progress
    const progressInterval = setInterval(() => {
      setGenerationProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 5;
      });
    }, 200);
  };

  const handleDownload = () => {
    if (imageData && imageData.image_base64) {
      const link = document.createElement('a');
      link.href = `data:image/png;base64,${imageData.image_base64}`;
      link.download = imageData.filename || 'generated_image.png';
      link.click();
    }
  };

  const presetPrompts = [
    "A futuristic city at sunset with flying cars",
    "A magical forest with glowing mushrooms",
    "A cyberpunk robot in neon colors",
    "A beautiful mountain landscape with snow peaks",
    "A steampunk airship flying over Victorian London"
  ];

  return (
    <div className="image-generation-widget">
      <div className="widget-header">
        <h3>🎨 AI Image Generation</h3>
        <button className="close-button" onClick={onClose}>×</button>
      </div>

      <div className="widget-content">
        {!imageData ? (
          <div className="generation-section">
            <div className="prompt-section">
              <h4>✨ Prompt</h4>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the image you want to generate..."
                rows={3}
                className="prompt-input"
              />
              
              <div className="preset-prompts">
                <h5>Quick Prompts:</h5>
                <div className="preset-buttons">
                  {presetPrompts.map((preset, index) => (
                    <button
                      key={index}
                      onClick={() => setPrompt(preset)}
                      className="preset-button"
                    >
                      {preset}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="settings-section">
              <h4>⚙️ Settings</h4>
              
              <div className="setting-group">
                <label>Negative Prompt:</label>
                <input
                  type="text"
                  value={negativePrompt}
                  onChange={(e) => setNegativePrompt(e.target.value)}
                  placeholder="What to avoid in the image..."
                  className="setting-input"
                />
              </div>

              <div className="setting-row">
                <div className="setting-group">
                  <label>Width: {width}px</label>
                  <input
                    type="range"
                    min="512"
                    max="1024"
                    step="64"
                    value={width}
                    onChange={(e) => setWidth(parseInt(e.target.value))}
                    className="setting-slider"
                  />
                </div>

                <div className="setting-group">
                  <label>Height: {height}px</label>
                  <input
                    type="range"
                    min="512"
                    max="1024"
                    step="64"
                    value={height}
                    onChange={(e) => setHeight(parseInt(e.target.value))}
                    className="setting-slider"
                  />
                </div>
              </div>

              <div className="setting-row">
                <div className="setting-group">
                  <label>Steps: {steps}</label>
                  <input
                    type="range"
                    min="10"
                    max="50"
                    step="5"
                    value={steps}
                    onChange={(e) => setSteps(parseInt(e.target.value))}
                    className="setting-slider"
                  />
                </div>

                <div className="setting-group">
                  <label>Guidance: {guidance}</label>
                  <input
                    type="range"
                    min="1"
                    max="20"
                    step="0.5"
                    value={guidance}
                    onChange={(e) => setGuidance(parseFloat(e.target.value))}
                    className="setting-slider"
                  />
                </div>
              </div>
            </div>

            <div className="generation-controls">
              <button
                onClick={handleGenerateImage}
                disabled={!prompt.trim() || isGenerating}
                className="generate-button"
              >
                {isGenerating ? '🎨 Generating...' : '🎨 Generate Image'}
              </button>

              {isGenerating && (
                <div className="generation-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${generationProgress}%` }}
                    ></div>
                  </div>
                  <p>Generating your masterpiece... {generationProgress}%</p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="result-section">
            <div className="image-display">
              <img
                src={`data:image/png;base64,${imageData.image_base64}`}
                alt="Generated image"
                className="generated-image"
              />
            </div>

            <div className="image-info">
              <h4>📋 Image Information</h4>
              <p><strong>Prompt:</strong> {imageData.prompt}</p>
              {imageData.negative_prompt && (
                <p><strong>Negative Prompt:</strong> {imageData.negative_prompt}</p>
              )}
              <p><strong>Size:</strong> {imageData.width} × {imageData.height}px</p>
              <p><strong>Steps:</strong> {imageData.num_inference_steps}</p>
              <p><strong>Guidance:</strong> {imageData.guidance_scale}</p>
              <p><strong>Generated:</strong> {imageData.generated_at}</p>
            </div>

            <div className="image-actions">
              <button onClick={handleDownload} className="action-button">
                💾 Download Image
              </button>
              <button 
                onClick={() => {
                  setPrompt('');
                  setNegativePrompt('');
                  if (window.socket) {
                    window.socket.emit('clear_image_data');
                  }
                }} 
                className="action-button"
              >
                🎨 Generate New Image
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageGenerationWidget;
