"use client";

import { useState } from "react";
import { MessageList } from "./MessageList";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { sendChatMessage } from "@/lib/api";
import { parseResponse, type ParsedResponse } from "@/lib/parser";

interface Message {
  role: "user" | "assistant";
  content: string;
  parsed: ParsedResponse;
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showRaw, setShowRaw] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setLoading(true);

    setMessages((prev) => [...prev, { role: "user", content: userMessage, parsed: { type: "text", content: userMessage } }]);

    try {
      const response = await sendChatMessage(userMessage);
      const parsed = parseResponse(response);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response, parsed },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${error instanceof Error ? error.message : "Unknown error"}`,
          parsed: { type: "text", content: `Error: ${error}` },
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <MessageList messages={messages} isLoading={loading} />

      <div className="border-t border-slate-800 p-4 space-y-3">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Query market data, run backtests, detect anomalies..."
            disabled={loading}
            className="bg-slate-950 border-slate-800"
          />
          <Button type="submit" disabled={loading || !input.trim()} className="shrink-0">
            Send
          </Button>
        </form>

        <div className="flex items-center gap-4 text-xs">
          <label className="flex items-center gap-2 text-slate-500 cursor-pointer hover:text-slate-400">
            <input
              type="checkbox"
              checked={showRaw}
              onChange={(e) => setShowRaw(e.target.checked)}
              className="rounded border-slate-700 bg-slate-900"
            />
            Show raw JSON
          </label>
        </div>
      </div>
    </div>
  );
}