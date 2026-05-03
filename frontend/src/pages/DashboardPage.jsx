import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import VideoUploader from '../components/VideoUploader';
import ResultsPanel from '../components/ResultsPanel';

function DashboardPage() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [result, setResult] = useState(null);

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center',
                          borderBottom:'2px solid #1B3A6B', paddingBottom:'1rem', marginBottom:'2rem' }}>
                <div>
                    <h1 style={{ margin:0, color:'#1B3A6B' }}>Silent Voices</h1>
                    <p style={{ margin:0, color:'#666' }}>
                        Welcome, <strong>{user?.full_name}</strong>
                    </p>
                </div>
                <button onClick={() => { logout(); navigate('/login'); }}
                    style={{ padding:'0.5rem 1rem', background:'#cc0000',
                             color:'white', border:'none', borderRadius:'6px', cursor:'pointer' }}>
                    Log Out
                </button>
            </div>

            <h2 style={{ color:'#0D7377' }}>Upload ASL Video for Translation</h2>
            <p style={{ color:'#555' }}>
                Record yourself performing ASL signs, upload the video, and the system
                will translate the gestures into English text.
            </p>

            <VideoUploader onResult={(r) => setResult(r)} />

            {result && <ResultsPanel result={result} />}
        </div>
    );
}

export default DashboardPage;