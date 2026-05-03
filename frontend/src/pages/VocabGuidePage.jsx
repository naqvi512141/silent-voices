// VocabGuidePage.jsx
// Shows all supported ASL signs with descriptions.
// Includes a search bar for filtering by label or description.

import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';

const API_URL = 'http://localhost:8000';

function VocabGuidePage() {
    const [vocab, setVocab]     = useState([]);
    const [search, setSearch]   = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`${API_URL}/vocabulary/`)
            .then(r => r.json())
            .then(d => setVocab(d.vocabulary))
            .finally(() => setLoading(false));
    }, []);

    const filtered = vocab.filter(v =>
        v.label.toLowerCase().includes(search.toLowerCase()) ||
        v.description.toLowerCase().includes(search.toLowerCase())
    );

    const letters = filtered.filter(v => v.type === 'letter');
    const controls = filtered.filter(v => v.type === 'control');

    return (
        <>
            <Navbar />
            <a href="#main-content" className="skip-link">Skip to content</a>

            <main id="main-content" style={{ maxWidth: '960px', margin: '2rem auto',
                                             padding: '0 1rem' }}>
                <h1 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                    ASL Vocabulary Guide
                </h1>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                    All signs currently supported by the Silent Voices recognition model.
                    Perform each sign clearly and hold it for at least half a second.
                </p>

                {/* Search bar — aria-label for screen readers */}
                <input
                    type="search"
                    placeholder="Search signs..."
                    aria-label="Search vocabulary"
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    style={{ maxWidth: '360px', marginBottom: '1.5rem' }}
                />

                {loading && <p style={{ color: 'var(--text-muted)' }}>Loading vocabulary...</p>}

                {/* Letters section */}
                {letters.length > 0 && (
                    <section aria-labelledby="letters-heading">
                        <h2 id="letters-heading"
                            style={{ color: 'var(--accent-teal)', marginBottom: '1rem' }}>
                            ASL Alphabet ({letters.length} signs)
                        </h2>
                        <div style={{ display: 'grid',
                                      gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))',
                                      gap: '0.75rem', marginBottom: '2rem' }}>
                            {letters.map(sign => (
                                <div key={sign.id} className="card"
                                     style={{ textAlign: 'center', padding: '1rem 0.75rem' }}>
                                    {/* Large letter display */}
                                    <div style={{ fontSize: '2.5rem', fontWeight: '900',
                                                  color: 'var(--accent-navy)',
                                                  marginBottom: '0.4rem',
                                                  lineHeight: 1 }}>
                                        {sign.label}
                                    </div>
                                    {/* Placeholder for hand diagram image */}
                                    <div style={{ background: 'var(--bg-secondary)',
                                                  borderRadius: '6px', height: '80px',
                                                  display: 'flex', alignItems: 'center',
                                                  justifyContent: 'center',
                                                  marginBottom: '0.5rem',
                                                  border: '1px dashed var(--border-color)' }}>
                                        <span style={{ fontSize: '0.7rem',
                                                       color: 'var(--text-muted)',
                                                       textAlign: 'center', padding: '0 4px' }}>
                                            🤟 Hand diagram
                                        </span>
                                    </div>
                                    <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)',
                                                lineHeight: '1.3' }}>
                                        {sign.description}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* Control signs */}
                {controls.length > 0 && (
                    <section aria-labelledby="controls-heading">
                        <h2 id="controls-heading"
                            style={{ color: 'var(--accent-teal)', marginBottom: '1rem' }}>
                            Control Signs
                        </h2>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            {controls.map(sign => (
                                <div key={sign.id} className="card"
                                     style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                    <span className="badge badge-navy"
                                          style={{ minWidth: '80px', textAlign: 'center',
                                                   fontSize: '0.85rem' }}>
                                        {sign.label}
                                    </span>
                                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem',
                                                margin: 0 }}>
                                        {sign.description}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {!loading && filtered.length === 0 && (
                    <p style={{ color: 'var(--text-muted)' }}>
                        No signs match your search.
                    </p>
                )}
            </main>
        </>
    );
}

export default VocabGuidePage;