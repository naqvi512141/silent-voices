import React, { useState } from 'react';
import VideoUploader from '../components/VideoUploader';
import ResultsPanel from '../components/ResultsPanel';
import Navbar from '../components/Navbar'; 

function DashboardPage() {
    // We removed 'const { user } = useAuth();' because user info is now 
    // handled inside the <Navbar /> component.
    const [result, setResult] = useState(null);

    return (
        <>
            {/* The Navbar component automatically accesses useAuth to show the name */}
            <Navbar />
            
            <a href="#main-content" className="skip-link">Skip to content</a>

            <main id="main-content" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
                
                <h2 style={{ color: 'var(--accent-teal)', marginTop: '1rem' }}>
                    Upload ASL Video for Translation
                </h2>
                
                <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                    Record yourself performing ASL signs, upload the video, and the system 
                    will translate the gestures into English text.
                </p>

                <VideoUploader onResult={(r) => setResult(r)} />

                {result && <ResultsPanel result={result} />}
                
            </main>
        </>
    );
}

export default DashboardPage;