import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('pdf_file');
    
    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }
    
    // Use the backend URL instead of calling itself
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    const response = await fetch(`${backendUrl}/upload_file`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Backend upload error:', errorText);
      return NextResponse.json({ success: false, error: errorText }, { status: response.status });
    }
    
    const data = await response.json();
    return NextResponse.json({ success: true, data });
  } catch (error) {
    console.error('File upload error:', error);
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Add CORS support for preflight requests
export async function OPTIONS(request: Request) {
  const nextResponse = NextResponse.json({}, { status: 200 });
  
  // Set CORS headers
  nextResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  nextResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Accept');
  nextResponse.headers.set('Access-Control-Allow-Credentials', 'true');
  
  // Use dynamic origin
  const origin = request.headers.get('origin') || '*';
  nextResponse.headers.set('Access-Control-Allow-Origin', origin);
  
  return nextResponse;
}
