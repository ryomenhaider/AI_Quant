"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { BacktestData } from "@/lib/parser";
import { TrendingUp, TrendingDown, BarChart3, Activity } from "lucide-react";

interface BacktestCardProps {
  data: BacktestData;
}

export function BacktestCard({ data }: BacktestCardProps) {
  const isProfitable = data.pnl > 0;
  const isHighSharpe = data.sharpe > 1;
  const isHighDrawdown = data.max_drawdown < -10;

  return (
    <Card className="w-full max-w-md bg-slate-900 border-slate-800">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-slate-200">
            {data.strategy.replace(/_/g, " ").toUpperCase()}
          </CardTitle>
          <Badge variant={isProfitable ? "success" : "danger"}>
            {isProfitable ? "+" : ""}
            {data.pnl.toFixed(2)}%
          </Badge>
        </div>
        <CardDescription className="text-slate-400">{data.symbol}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          <Metric
            icon={<TrendingUp className="h-4 w-4 text-emerald-400" />}
            label="PnL"
            value={`${isProfitable ? "+" : ""}${data.pnl.toFixed(2)}%`}
            positive={isProfitable}
            negative={!isProfitable}
          />
          <Metric
            icon={<Activity className="h-4 w-4 text-blue-400" />}
            label="Sharpe"
            value={data.sharpe.toFixed(2)}
            positive={isHighSharpe}
          />
          <Metric
            icon={<TrendingDown className="h-4 w-4 text-red-400" />}
            label="Max DD"
            value={`${data.max_drawdown.toFixed(2)}%`}
            negative={isHighDrawdown}
          />
          <Metric
            icon={<BarChart3 className="h-4 w-4 text-slate-400" />}
            label="Trades"
            value={data.trades.toString()}
          />
        </div>
        {data.params && Object.keys(data.params).length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-800">
            <div className="flex flex-wrap gap-2">
              {Object.entries(data.params).map(([key, value]) => (
                <span
                  key={key}
                  className="text-xs text-slate-500 bg-slate-950 px-2 py-1 rounded"
                >
                  {key}: {value}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function Metric({
  icon,
  label,
  value,
  positive,
  negative,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  positive?: boolean;
  negative?: boolean;
}) {
  return (
    <div className="flex items-center gap-2">
      {icon}
      <div>
        <div className="text-xs text-slate-500">{label}</div>
        <div
          className={`text-sm font-semibold ${
            positive
              ? "text-emerald-400"
              : negative
              ? "text-red-400"
              : "text-slate-200"
          }`}
        >
          {value}
        </div>
      </div>
    </div>
  );
}