// ResultsPanel.jsx — Displays the translation result with TTS and confidence info

import React, { useState } from 'react';

function ResultsPanel({ result }) {
    const [isSpeaking, setIsSpeaking] = useState(false);

    const speak = () => {
        if (!window.speechSynthesis) {
            alert('Text-to-speech is not supported in your browser.');
            return;
        }
        window.speechSynthesis.cancel();  // Stop any currently playing speech
        const utterance = new SpeechSynthesisUtterance(result.translated_text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;            // Slightly slower than default
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        window.speechSynthesis.speak(utterance);
    };

    return (
        <div style={{ maxWidth: '600px', margin: '2rem auto',
                      border: '1px solid #DDDDDD', borderRadius: '12px',
                      padding: '1.5rem', background: 'white' }}>

            <h3 style={{ color: '#1B3A6B', marginTop: 0 }}>Translation Result</h3>

            {/* Main translated text */}
            <div style={{ background: '#F0F8FF', borderRadius: '8px',
                          padding: '1.5rem', marginBottom: '1rem',
                          border: '1px solid #D6E4F0' }}>
                <p style={{ fontSize: '1.4rem', fontWeight: 'bold',
                             color: '#1B3A6B', margin: 0, letterSpacing: '0.05em' }}>
                    {result.translated_text}
                </p>
            </div>

            {/* Stats row */}
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <div style={{ flex: 1, background: '#F8F8F8', borderRadius: '6px',
                               padding: '0.75rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#0D7377' }}>
                        {result.avg_confidence}%
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>Avg. Confidence</div>
                </div>
                <div style={{ flex: 1, background: '#F8F8F8', borderRadius: '6px',
                               padding: '0.75rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#0D7377' }}>
                        {result.frames_with_hands}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>Frames with Hands</div>
                </div>
                <div style={{ flex: 1, background: '#F8F8F8', borderRadius: '6px',
                               padding: '0.75rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#0D7377' }}>
                        {result.gesture_sequence?.filter(g => g.label).length}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>Gestures Found</div>
                </div>
            </div>

            {/* TTS Button */}
            <button onClick={speak} disabled={isSpeaking}
                style={{ width: '100%', padding: '0.75rem',
                         background: isSpeaking ? '#888' : '#0D7377',
                         color: 'white', border: 'none', borderRadius: '8px',
                         fontSize: '1rem', cursor: isSpeaking ? 'default' : 'pointer',
                         marginBottom: '1rem' }}>
                {isSpeaking ? '🔊 Speaking...' : '🔊 Read Aloud (Text-to-Speech)'}
            </button>

            {/* Gesture breakdown */}
            {result.gesture_sequence && result.gesture_sequence.length > 0 && (
                <div>
                    <p style={{ fontWeight: 'bold', color: '#444', marginBottom: '0.5rem' }}>
                        Gesture Breakdown:
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                        {result.gesture_sequence
                            .filter(g => g.label)
                            .map((g, i) => (
                                <div key={i} style={{
                                    background: '#1B3A6B', color: 'white',
                                    borderRadius: '6px', padding: '0.4rem 0.75rem',
                                    fontSize: '0.85rem', textAlign: 'center'
                                }}>
                                    <div style={{ fontWeight: 'bold' }}>{g.label}</div>
                                    <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>
                                        {g.confidence}%
                                    </div>
                                </div>
                            ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResultsPanel;