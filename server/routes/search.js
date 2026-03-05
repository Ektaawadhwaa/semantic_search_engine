import express from 'express'
import axios from 'axios'

const router = express.Router()

router.post('/', async (req, res) => {
  const { query } = req.body

  if (!query) {
    return res.status(400).json({ error: 'query is required' })
  }

  try {
    // call Python Flask API
    const response = await axios.post(
      `${process.env.PYTHON_API_URL}/search`,
      { query }
    )

    res.json(response.data)

  } catch (error) {
    console.error('Python API error:', error.message)
    res.status(500).json({ error: 'Search service unavailable' })
  }
})

export default router
