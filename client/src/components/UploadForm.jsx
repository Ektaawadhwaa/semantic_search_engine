import { useState } from 'react'
import axios from 'axios'

const API_URL = 'https://semantic-search-node.onrender.com'

const UploadForm = ({ onUploaded }) => {
    const [text, setText] = useState('')
    const [category, setCategory] = useState('general')
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState('')

    const handleUpload = async () => {
        if (!text.trim()) return

        setLoading(true)
        setMessage('')

        try {
            await axios.post(`${API_URL}/api/ingest`, {
                text,
                category,
                date: new Date().toISOString().split('T')[0]
            })
            setMessage('Document uploaded successfully! ✅')
            setText('')
            if (onUploaded) onUploaded()
        } catch (err) {
            setMessage('Upload failed. Try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{
            padding: '20px',
            marginBottom: '24px',
            borderRadius: '8px',
            border: '1px solid #ddd',
            background: '#f9f9f9'
        }}>
            <h3 style={{ margin: '0 0 12px' }}>📄 Add Document</h3>

            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your document text here..."
                rows={4}
                style={{
                    width: '100%',
                    padding: '10px',
                    borderRadius: '6px',
                    border: '1px solid #ccc',
                    fontSize: '14px',
                    marginBottom: '10px',
                    boxSizing: 'border-box'
                }}
            />

            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    style={{
                        padding: '8px',
                        borderRadius: '6px',
                        border: '1px solid #ccc',
                        fontSize: '14px'
                    }}
                >
                    <option value="general">General</option>
                    <option value="technology">Technology</option>
                    <option value="finance">Finance</option>
                    <option value="sports">Sports</option>
                    <option value="science">Science</option>
                </select>

                <button
                    onClick={handleUpload}
                    disabled={loading}
                    style={{
                        padding: '8px 20px',
                        borderRadius: '6px',
                        background: '#2196F3',
                        color: 'white',
                        border: 'none',
                        fontSize: '14px',
                        cursor: loading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Uploading...' : 'Upload'}
                </button>

                {message && (
                    <span style={{ fontSize: '14px', color: message.includes('✅') ? 'green' : 'red' }}>
                        {message}
                    </span>
                )}
            </div>
        </div>
    )
}

export default UploadForm