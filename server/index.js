import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import searchRoute from './routes/search.js'
import ingestRoute from './routes/ingest.js' 

dotenv.config()

const app = express()

app.use(cors())
app.use(express.json())
app.use('/api/ingest', ingestRoute)                
app.use('/api/search', searchRoute)

app.get('/health', (req, res) => {
  res.json({ status: 'ok' })
})

const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})

