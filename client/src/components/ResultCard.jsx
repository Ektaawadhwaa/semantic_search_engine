const ResultCard = ({ text, category, score }) => {
  return (
    <div style={{
      padding: '16px',
      marginBottom: '12px',
      borderRadius: '8px',
      border: '1px solid #ddd',
      background: '#fff',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
    }}>
      <p style={{ fontSize: '16px', margin: '0 0 10px' }}>{text}</p>
      <div style={{ display: 'flex', gap: '12px' }}>
        <span style={{
          background: '#e3f2fd',
          padding: '4px 10px',
          borderRadius: '20px',
          fontSize: '13px'
        }}>
          📁 {category}
        </span>
        <span style={{
          background: '#e8f5e9',
          padding: '4px 10px',
          borderRadius: '20px',
          fontSize: '13px'
        }}>
          🎯 Score: {score.toFixed(3)}
        </span>
      </div>
    </div>
  )
}

export default ResultCard