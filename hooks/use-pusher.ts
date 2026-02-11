import { useEffect, useState } from 'react';
import Pusher from 'pusher-js';

// Global Singleton Pattern: Prevents multiple socket connections on re-render
let pusherClient: Pusher | null = null;

export const usePusher = (channelName: string, eventName: string) => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    // Initialize once and reuse for the entire session
    if (!pusherClient) {
      pusherClient = new Pusher('7e21a4ce1acbb42bd97d', {
        cluster: 'ap2', // Forced Mumbai cluster to match API
        forceTLS: true
      });
    }

    const channel = pusherClient.subscribe(channelName);
    
    const handler = (payload: any) => {
      console.log("[SYNAPSE] Telemetry Inbound:", payload.fileName);
      setData(payload);
    };

    channel.bind(eventName, handler);

    return () => {
      // Clean up bindings but keep the connection alive for speed
      channel.unbind(eventName, handler);
      pusherClient?.unsubscribe(channelName);
    };
  }, [channelName, eventName]);

  return data;
};
