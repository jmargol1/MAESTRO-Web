import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    // Get the file from formData
    const formData = await request.formData();
    const file = formData.get('pdf_file');
    
    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }
    
    const backendUrl = process.env.NEXT_API_REWRITES_BACKEND_URL || 'http://backend:8080';
    
    // Make a preliminary request to fetch the API key status
    const checkResponse = await fetch(`${backendUrl}/check_session`, {
      method: 'GET',
      headers: {
        'Cookie': request.headers.get('cookie') || '',
      },
      credentials: 'include',
    });
    
    const checkData = await checkResponse.json();
    console.log('API key status check:', checkData);
    
    // If API key is not set, return error immediately
    if (!checkData.api_key_set) {
      return NextResponse.json({ 
        success: false, 
        error: 'API key not set. Please set your API key first.' 
      }, { status: 401 });
    }
    
    // Forward the upload with cookies
    const response = await fetch(`${backendUrl}/upload_file`, {
      method: 'POST',
      headers: {
        'Cookie': request.headers.get('cookie') || '',
      },
      body: formData,
      credentials: 'include',
    });
    
    if (!response.ok) {
      let errorText = await response.text();
      console.error('Backend upload error:', errorText, response.status);
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
