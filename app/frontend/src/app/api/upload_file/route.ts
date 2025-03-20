import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('pdf_file');
    
    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }
    
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    
    // Create a new FormData object to add the API key explicitly
    const newFormData = new FormData();
    newFormData.append('pdf_file', file);
    
    // Try to get API key from cookies
    const cookieStore = cookies();
    const apiKeyCookie = cookieStore.get('api_key');
    
    // If we have an API key from cookies, add it to the form data
    if (apiKeyCookie && apiKeyCookie.value) {
      newFormData.append('api_key', apiKeyCookie.value);
    }
    
    // Alternatively, try to extract it from request cookies header
    const cookieHeader = request.headers.get('cookie');
    if (cookieHeader && !apiKeyCookie) {
      const match = cookieHeader.match(/api_key=([^;]+)/);
      if (match && match[1]) {
        newFormData.append('api_key', match[1]);
      }
    }
    
    // You might need to check your backend code to see exactly how it expects to receive authentication
    
    const response = await fetch(`${backendUrl}/upload_file`, {
      method: 'POST',
      headers: {
        // Forward authentication cookies
        'Cookie': request.headers.get('cookie') || '',
      },
      body: newFormData,
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
