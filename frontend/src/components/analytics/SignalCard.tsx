"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { AnomalyData } from "@/lib/parser";
import { AlertTriangle, Shield, Zap, Activity } from "lucide-react";

interface SignalCardProps {
  data: AnomalyData;
}

export function SignalCard({ data }: SignalCardProps) {
  const typeConfig = {
    spoofing: {
      color: "danger",
      icon: Shield,
      label: "SPOOFING",
    },
    absorption: {
      color: "warning",
      icon: AlertTriangle,
      label: "ABSORPTION",
    },
    aggressive_flow: {
      color: "warning",
      icon: Zap,
      label: "AGGRESSIVE FLOW",
    },
  };

  const config = typeConfig[data.type] || typeConfig.aggressive_flow;
  const Icon = config.icon;
  const confidencePct = Math.round(data.confidence * 100);

  return (
    <Card className="w-full max-w-md bg-slate-900 border-slate-800">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Icon className={`h-4 w-4 ${data.type === "spoofing" ? "text-red-400" : "text-amber-400"}`} />
            <CardTitle className="text-sm font-medium text-slate-200">{config.label}</CardTitle>
          </div>
          <Badge variant={config.color as "danger" | "warning"}>
            {confidencePct}% confidence
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <p className="text-sm text-slate-300 leading-relaxed">{data.explanation}</p>
          
          <div className="flex items-center gap-4 text-xs text-slate-500">
            {data.price_level > 0 && (
              <span className="flex items-center gap-1">
                <span className="text-slate-600">Price:</span>
                <span className="text-slate-400">{data.price_level.toLocaleString()}</span>
              </span>
            )}
            {data.side && (
              <span className="flex items-center gap-1">
                <span className="text-slate-600">Side:</span>
                <span className={`uppercase ${data.side === "buy" || data.side === "bid" ? "text-emerald-400" : "text-red-400"}`}>
                  {data.side}
                </span>
              </span>
            )}
          </div>

          <div className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className="text-slate-500">Confidence</span>
              <span className="text-slate-400">{confidencePct}%</span>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className={`h-full ${
                  confidencePct > 70 ? "bg-red-400" : confidencePct > 40 ? "bg-amber-400" : "bg-slate-400"
                }`}
                style={{ width: `${confidencePct}%` }}
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}