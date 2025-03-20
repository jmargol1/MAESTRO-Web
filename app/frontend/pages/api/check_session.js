export default async function handler(req, res) {
  const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://localhost:8080';
  console.log('Backend URL:', backendUrl);
  
  try {
    const response = await fetch(`${backendUrl}/check_session`);
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('Error proxying to backend:', error);
    res.status(500).json({ error: 'Failed to connect to backend' });
  }
}
