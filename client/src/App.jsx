import { useState } from 'react'
import axios from 'axios'
import SearchBar from './components/SearchBar'
import ResultCard from './components/ResultCard'

const API_URL = 'http://localhost:5000'

export default function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searched, setSearched] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return

    setLoading(true)
    setError('')
    setSearched(true)

    try {
      const response = await axios.post(`${API_URL}/api/search`, { query })
      setResults(response.data.results)
    } catch (err) {
      setError('Search failed. Make sure the server is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '40px 20px',
      fontFamily: 'sans-serif'
    }}>
      <h1 style={{ textAlign: 'center', marginBottom: '8px' }}>
        🔍 Semantic Search Engine
      </h1>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '32px' }}>
        Search by meaning, not just keywords
      </p>

      <SearchBar
        query={query}
        setQuery={setQuery}
        onSearch={handleSearch}
        loading={loading}
      />

      {error && (
        <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>
      )}

      {searched && !loading && results.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666' }}>No results found.</p>
      )}

      {results.map((result, index) => (
        <ResultCard
          key={index}
          text={result.text}
          category={result.category}
          score={result.score}
        />
      ))}
    </div>
  )
}