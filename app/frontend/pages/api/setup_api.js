export default async function handler(req, res) {
  const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://localhost:8080';
  console.log('Backend URL for API setup:', backendUrl);
  
  try {
    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/setup_api`, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body),
    });
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }
    
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('Error setting up API:', error);
    res.status(500).json({ error: 'Failed to set up API key' });
  }
}
