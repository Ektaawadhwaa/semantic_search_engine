const SearchBar = ({ query, setQuery, onSearch, loading }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') onSearch()
  }

  return (
    <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search documents..."
        style={{
          flex: 1,
          padding: '12px',
          fontSize: '16px',
          borderRadius: '8px',
          border: '1px solid #ccc'
        }}
      />
      <button
        onClick={onSearch}
        disabled={loading}
        style={{
          padding: '12px 24px',
          fontSize: '16px',
          borderRadius: '8px',
          background: '#4CAF50',
          color: 'white',
          border: 'none',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Searching...' : 'Search'}
      </button>
    </div>
  )
}

export default SearchBar