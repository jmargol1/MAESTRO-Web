import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  try {
    const { api_key } = await request.json();
    
    if (!api_key) {
      return NextResponse.json({ success: false, error: 'API key is required' }, { status: 400 });
    }

    const response = await fetch('http://backend:8080/setup_api', { // Updated URL
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ api_key }),
    });

    console.log('Response status:', response.status);
    const responseText = await response.text();
    console.log('Response text:', responseText);

    if (!response.ok) {
      return NextResponse.json({ success: false, error: responseText || 'Server error' }, { status: response.status });
    }

    let data;
    try {
      data = JSON.parse(responseText);
    } catch (e) {
      console.error('Failed to parse JSON response:', e);
      data = { message: responseText };
    }
    
    // Set the response with proper CORS headers
    const nextResponse = NextResponse.json({ success: true, data });
    nextResponse.headers.set('Access-Control-Allow-Credentials', 'true');
    nextResponse.headers.set('Access-Control-Allow-Origin', 'http://localhost:3002');
    
    return nextResponse;
  } catch (error) {
    console.error('API Setup Error:', error);
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Handle CORS preflight requests
export async function OPTIONS(request: Request) {
  const nextResponse = NextResponse.json({}, { status: 200 });
  
  // Set CORS headers
  nextResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  nextResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Accept');
  nextResponse.headers.set('Access-Control-Allow-Credentials', 'true');
  nextResponse.headers.set('Access-Control-Allow-Origin', 'http://localhost:3002');
  
  return nextResponse;
}
