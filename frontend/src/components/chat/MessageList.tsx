"use client";

import { useEffect, useRef } from "react";
import { MessageBubble } from "./MessageBubble";
import type { ParsedResponse } from "@/lib/parser";

interface Message {
  role: "user" | "assistant";
  content: string;
  parsed: ParsedResponse;
}

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && (
        <div className="text-center mt-16">
          <h2 className="text-xl font-semibold text-slate-300 mb-2">AI Quant Analyst</h2>
          <p className="text-slate-500 text-sm">
            Query market data, run backtests, or detect anomalies
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-2 text-xs text-slate-600">
            <ExampleQuery>What's BTC price?</ExampleQuery>
            <ExampleQuery>Backtest BTC breakout</ExampleQuery>
            <ExampleQuery>Any spoofing?</ExampleQuery>
          </div>
        </div>
      )}

      {messages.map((msg, i) => (
        <MessageBubble key={i} role={msg.role} content={msg.content} parsed={msg.parsed} />
      ))}

      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-slate-900 rounded-lg p-4">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}

function ExampleQuery({ children }: { children: React.ReactNode }) {
  return (
    <span className="bg-slate-900 px-3 py-1.5 rounded-full text-slate-500 border border-slate-800">
      {children}
    </span>
  );
}