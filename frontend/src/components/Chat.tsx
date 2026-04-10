'use client';

import { useState, useRef, useEffect } from 'react';
import { Message, BacktestCard, SignalCard } from './Message';

interface MessageData {
  role: 'user' | 'assistant';
  content: string;
  structuredData?: any;
}

export function Chat() {
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showTools, setShowTools] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);

    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      const responseText = data.response || JSON.stringify(data);

      let structuredData = null;
      
      try {
        const parsed = JSON.parse(responseText);
        if (parsed.pnl !== undefined) {
          structuredData = parsed;
        } else if (parsed.type && ['spoofing', 'absorption', 'aggressive_flow'].includes(parsed.type)) {
          structuredData = parsed;
        } else if (parsed.data && Array.isArray(parsed.data) && parsed.data.length > 0) {
          structuredData = parsed.data[0];
        }
      } catch {
        // Not JSON, use as plain text
      }

      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: responseText,
        structuredData 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Error: ${error}` 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <h2 className="text-xl font-semibold mb-2">AI Quant Analyst</h2>
            <p>Ask about market data, backtests, or anomaly detection</p>
          </div>
        )}
        
        {messages.map((msg, i) => (
          <Message key={i} {...msg} />
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-gray-800 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about BTC, backtests, anomalies..."
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-600"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Send
          </button>
        </form>
        
        <div className="flex items-center gap-4 mt-3">
          <label className="flex items-center gap-2 text-sm text-gray-500 cursor-pointer">
            <input
              type="checkbox"
              checked={showTools}
              onChange={(e) => setShowTools(e.target.checked)}
              className="rounded border-gray-700"
            />
            Show tool calls
          </label>
        </div>
      </div>
    </div>
  );
}