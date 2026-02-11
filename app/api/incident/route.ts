import { NextResponse } from 'next/server';
import Pusher from 'pusher';

export async function POST(req: Request) {
  try {
    const auth = req.headers.get('x-agent-secret');
    
    // Hardened Secret Check from Environment
    if (auth !== process.env.AGENT_SECRET_TOKEN) {
      return NextResponse.json({ error: 'UNAUTHORIZED' }, { status: 401 });
    }

    // Explicitly configured Pusher instance to prevent cluster mismatch
    const pusher = new Pusher({
      appId: process.env.PUSHER_APP_ID!,
      key: process.env.NEXT_PUBLIC_PUSHER_KEY!,
      secret: process.env.PUSHER_SECRET!,
      cluster: 'ap2', // HARDCODED STABILITY: Mumbai Cluster
      useTLS: true,
    });

    const payload = await req.json();

    // Broadcast the threat with extended metadata for Feb 14 UI
    await pusher.trigger('critical-alert', 'threat-detected', {
      ...payload,
      status: 'ENFORCE', 
      mitigated: true,
      serverTimestamp: Date.now()
    });

    return NextResponse.json({ success: true });
  } catch (e) {
    console.error("Critical Inbound Error:", e);
    return NextResponse.json({ error: 'INTERNAL_SERVER_ERROR' }, { status: 500 });
  }
}
