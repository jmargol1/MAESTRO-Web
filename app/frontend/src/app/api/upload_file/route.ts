import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('pdf_file');

    if (!file) {
      return NextResponse.json({ success: false, error: 'File is required' }, { status: 400 });
    }

    const response = await fetch('/api/upload_file', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.text();
      return NextResponse.json({ success: false, error }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json({ success: true, data });
  } catch (error) {
    console.error('File Upload Error:', error);
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}
