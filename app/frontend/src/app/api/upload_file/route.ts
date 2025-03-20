import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('pdf_file');
    
    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }
    
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    
    // Forward the request directly without trying to iterate headers
    const response = await fetch(`${backendUrl}/upload_file`, {
      method: 'POST',
      // Add authorization header if your backend expects it
      headers: {
        // You can add specific headers here if needed
        'Authorization': request.headers.get('authorization') || '',
        'Cookie': request.headers.get('cookie') || '',
      },
      body: formData,
      credentials: 'include',
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

export async function OPTIONS(request: Request) {
  const nextResponse = NextResponse.json({}, { status: 200 });
  
  nextResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  nextResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization');
  nextResponse.headers.set('Access-Control-Allow-Credentials', 'true');
  
  const origin = request.headers.get('origin') || '*';
  nextResponse.headers.set('Access-Control-Allow-Origin', origin);
  
  return nextResponse;
}
