import express from 'express'
import axios from 'axios'

const router = express.Router()

router.post('/', async (req, res) => {
    const { text, category, date } = req.body

    if (!text) {
        return res.status(400).json({ error: 'text is required' })
    }

    try {
        const response = await axios.post(
            `${process.env.PYTHON_API_URL}/ingest`,
            { text, category, date }
        )
        res.json(response.data)

    } catch (error) {
        console.error('Ingest error:', error.message)
        res.status(500).json({ error: 'Ingest service unavailable' })
    }
})

export default router