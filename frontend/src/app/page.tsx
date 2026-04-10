'use client';

import { Chat } from '@/components/Chat';

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-gray-100">
      <div className="max-w-4xl mx-auto h-screen flex flex-col">
        <div className="border-b border-gray-800 px-4 py-3">
          <h1 className="text-lg font-semibold">AI Quant Analyst</h1>
          <p className="text-sm text-gray-500">Crypto market analysis with tool orchestration</p>
        </div>
        
        <main className="flex-1 overflow-hidden">
          <Chat />
        </main>
      </div>
    </div>
  );
}