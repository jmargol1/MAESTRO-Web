import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('pdf_file');
    
    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }
    
    // Get API key from cookies if possible
    const cookieStore = cookies();
    const apiKeyCookie = cookieStore.get('api_key');
    
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    
    // Create a new FormData to include everything
    const newFormData = new FormData();
    newFormData.append('pdf_file', file);
    
    // Include API key if available from cookies
    if (apiKeyCookie && apiKeyCookie.value) {
      newFormData.append('api_key', apiKeyCookie.value);
    }
    
    const response = await fetch(`${backendUrl}/upload_file`, {
      method: 'POST',
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
