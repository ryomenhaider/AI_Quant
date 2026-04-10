"use client";

import { cn } from "@/lib/parser";
import { BacktestCard } from "@/components/analytics/BacktestCard";
import { SignalCard } from "@/components/analytics/SignalCard";
import type { ParsedResponse } from "@/lib/parser";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  parsed: ParsedResponse;
}

export function MessageBubble({ role, content, parsed }: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={cn("flex", isUser ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "max-w-[85%] rounded-lg p-3 text-sm",
          isUser
            ? "bg-blue-600 text-white"
            : "bg-transparent text-slate-100"
        )}
      >
        {parsed.type === "backtest" && parsed.backtest && (
          <BacktestCard data={parsed.backtest} />
        )}
        {parsed.type === "anomaly" && parsed.anomaly && (
          <SignalCard data={parsed.anomaly} />
        )}
        {(parsed.type === "text" || parsed.type === "unknown") && (
          <div className="whitespace-pre-wrap leading-relaxed">{parsed.content || content}</div>
        )}
      </div>
    </div>
  );
}