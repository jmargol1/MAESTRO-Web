import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('pdf_file');
    
    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }
    
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    
    // Extract cookies from the original request
    const cookieHeader = request.headers.get('cookie') || '';
    
    // Create a completely new FormData with all the original data
    const newFormData = new FormData();
    newFormData.append('pdf_file', file);
    
    // Forward the request with cookies for session-based auth
    const response = await fetch(`${backendUrl}/upload_file`, {
      method: 'POST',
      headers: {
        'Cookie': cookieHeader,
      },
      body: newFormData,
      credentials: 'include',
    });
    
    if (!response.ok) {
      let errorText;
      try {
        errorText = await response.text();
      } catch (e) {
        errorText = `Error status: ${response.status}`;
      }
      console.error('Backend upload error:', errorText);
      return NextResponse.json({ success: false, error: errorText }, { status: response.status });
    }
    
    let data;
    try {
      data = await response.json();
    } catch (e) {
      const text = await response.text();
      data = { text };
    }
    
    return NextResponse.json({ success: true, ...data });
  } catch (error) {
    console.error('File upload error:', error);
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function OPTIONS(request: Request) {
  const nextResponse = NextResponse.json({}, { status: 200 });
  nextResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  nextResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization, Cookie');
  nextResponse.headers.set('Access-Control-Allow-Credentials', 'true');
  const origin = request.headers.get('origin') || '*';
  nextResponse.headers.set('Access-Control-Allow-Origin', origin);
  return nextResponse;
}
