// HistoryPage.jsx
// Shows all past translation sessions for the logged-in user.
// Each session can be expanded to see gesture details.
// Provides TXT and PDF export download links.

import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import { getHistory, getSessionDetail,
         exportTxt, exportPdf } from '../services/historyService';

function HistoryPage() {
    const { token } = useAuth();
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading]   = useState(true);
    const [expanded, setExpanded] = useState(null); // session id currently expanded
    const [detail, setDetail]     = useState(null);
    const [feedback, setFeedback] = useState({}); // { sessionId: 'submitted' }

    useEffect(() => {
        getHistory(token)
            .then(data => setSessions(data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [token]);

    const handleExpand = async (id) => {
        if (expanded === id) { setExpanded(null); setDetail(null); return; }
        setExpanded(id);
        const d = await getSessionDetail(id, token);
        setDetail(d);
    };

    const handleExport = async (id, format) => {
        const fn = format === 'pdf' ? exportPdf : exportTxt;
        const blob = await fn(id, token);
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href     = url;
        a.download = `translation_${id}.${format}`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <>
            <Navbar />
            {/* skip-to-content for WCAG 2.1 */}
            <a href="#main-content" className="skip-link">Skip to content</a>

            <main id="main-content" style={{ maxWidth: '860px', margin: '2rem auto',
                                             padding: '0 1rem' }}>
                <h1 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                    Translation History
                </h1>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                    Your past ASL translation sessions. Click any row to expand details.
                </p>

                {loading && <p style={{ color: 'var(--text-muted)' }}>Loading history...</p>}

                {!loading && sessions.length === 0 && (
                    <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
                            No translations yet. Upload a video on the dashboard to get started.
                        </p>
                    </div>
                )}

                {/* Session list */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {sessions.map(s => (
                        <div key={s.id} className="card"
                             style={{ cursor: 'pointer', transition: 'box-shadow 0.2s' }}>

                            {/* Summary row — clickable to expand */}
                            <div onClick={() => handleExpand(s.id)}
                                 role="button" tabIndex={0}
                                 aria-expanded={expanded === s.id}
                                 onKeyDown={e => e.key === 'Enter' && handleExpand(s.id)}
                                 style={{ display: 'flex', justifyContent: 'space-between',
                                          alignItems: 'flex-start', gap: '1rem' }}>
                                <div style={{ flex: 1 }}>
                                    <p style={{ fontWeight: '700', color: 'var(--text-primary)',
                                                marginBottom: '0.25rem', fontSize: '1.05rem' }}>
                                        {s.translated_text || 'No translation'}
                                    </p>
                                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                                        {new Date(s.created_at).toLocaleString()} &nbsp;·&nbsp;
                                        Confidence: <strong>{s.avg_confidence?.toFixed(1)}%</strong>
                                    </p>
                                </div>
                                <span style={{ color: 'var(--text-muted)', fontSize: '1.2rem',
                                               userSelect: 'none' }}>
                                    {expanded === s.id ? '▲' : '▼'}
                                </span>
                            </div>

                            {/* Expanded detail */}
                            {expanded === s.id && detail && detail.id === s.id && (
                                <div style={{ marginTop: '1rem', borderTop: '1px solid var(--border-color)',
                                              paddingTop: '1rem' }}>
                                    {/* Gesture badges */}
                                    <p style={{ fontWeight: '600', color: 'var(--text-primary)',
                                                marginBottom: '0.5rem' }}>
                                        Gesture Sequence:
                                    </p>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem',
                                                  marginBottom: '1rem' }}>
                                        {detail.gesture_results.map((g, i) => (
                                            <span key={i} className="badge badge-navy"
                                                  style={{ fontSize: '0.8rem' }}>
                                                {g.gesture_label} {g.confidence.toFixed(0)}%
                                            </span>
                                        ))}
                                    </div>

                                    {/* Export and Feedback buttons */}
                                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                        <button className="btn btn-ghost"
                                                onClick={() => handleExport(s.id, 'txt')}
                                                aria-label="Download as text file">
                                            📄 Export TXT
                                        </button>
                                        <button className="btn btn-ghost"
                                                onClick={() => handleExport(s.id, 'pdf')}
                                                aria-label="Download as PDF">
                                            📑 Export PDF
                                        </button>

                                        {/* Feedback buttons */}
                                        {!feedback[s.id] ? (
                                            <>
                                                <button className="btn btn-teal"
                                                        onClick={() => handleFeedback(s.id, 1)}
                                                        aria-label="Translation was correct">
                                                    👍 Correct
                                                </button>
                                                <button className="btn btn-danger"
                                                        onClick={() => handleFeedback(s.id, 0)}
                                                        aria-label="Translation was incorrect">
                                                    👎 Incorrect
                                                </button>
                                            </>
                                        ) : (
                                            <span className="badge badge-green">
                                                ✓ Feedback submitted
                                            </span>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </main>
        </>
    );

    async function handleFeedback(sessionId, rating) {
        try {
            const { submitFeedback } = await import('../services/historyService');
            await submitFeedback(sessionId, rating, null, token);
            setFeedback(prev => ({ ...prev, [sessionId]: 'submitted' }));
        } catch (e) { console.error(e); }
    }
}

export default HistoryPage;