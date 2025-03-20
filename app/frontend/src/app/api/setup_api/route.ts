import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  try {
    const { api_key } = await request.json();
    
    if (!api_key) {
      return NextResponse.json({ success: false, error: 'API key is required' }, { status: 400 });
    }

    // Use the environment variable for the backend URL instead of hardcoded value
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    
    const response = await fetch(`${backendUrl}/setup_api`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ api_key }),
    });

    const responseText = await response.text();
    if (!response.ok) {
      return NextResponse.json({ success: false, error: responseText || 'Server error' }, { status: response.status });
    }
    
    let data;
    try {
      data = JSON.parse(responseText);
    } catch (e) {
      data = { message: responseText };
    }
    
    // Set the response with proper CORS headers
    const nextResponse = NextResponse.json({ success: true, data });
    nextResponse.headers.set('Access-Control-Allow-Credentials', 'true');
    
    // Use dynamic origin instead of hardcoded localhost
    const origin = request.headers.get('origin') || '*';
    nextResponse.headers.set('Access-Control-Allow-Origin', origin);
    
    return nextResponse;
  } catch (error) {
    console.error('Error setting up API:', error);
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
  
  // Use dynamic origin instead of hardcoded localhost
  const origin = request.headers.get('origin') || '*';
  nextResponse.headers.set('Access-Control-Allow-Origin', origin);
  
  return nextResponse;
}
