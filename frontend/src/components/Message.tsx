import React from 'react';

interface MessageProps {
  role: 'user' | 'assistant';
  content: string;
  structuredData?: BacktestResult | AnomalyResult | null;
}

interface BacktestResult {
  symbol: string;
  strategy: string;
  params: Record<string, number>;
  pnl: number;
  sharpe: number;
  max_drawdown: number;
  trades: number;
}

interface AnomalyResult {
  type: string;
  confidence: number;
  side: string;
  price_level: number;
  explanation: string;
  metrics: Record<string, number>;
}

export function Message({ role, content, structuredData }: MessageProps) {
  const isUser = role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] rounded-lg p-4 ${
        isUser 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-800 text-gray-100'
      }`}>
        {structuredData ? (
          <StructuredOutput data={structuredData} />
        ) : (
          <p className="whitespace-pre-wrap">{content}</p>
        )}
      </div>
    </div>
  );
}

function StructuredOutput({ data }: { data: BacktestResult | AnomalyResult }) {
  if ('pnl' in data) {
    return <BacktestCard data={data as BacktestResult} />;
  }
  
  if ('type' in data && ['spoofing', 'absorption', 'aggressive_flow'].includes(data.type)) {
    return <SignalCard data={data as AnomalyResult} />;
  }
  
  return <p>{JSON.stringify(data)}</p>;
}

export function BacktestCard({ data }: { data: BacktestResult }) {
  return (
    <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium text-gray-300">Backtest Result</span>
        <span className="text-xs text-gray-500">{data.symbol} · {data.strategy}</span>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <Metric label="PnL" value={`${data.pnl}%`} positive={data.pnl > 0} />
        <Metric label="Sharpe" value={data.sharpe.toFixed(2)} />
        <Metric label="Max DD" value={`${data.max_drawdown}%`} negative />
        <Metric label="Trades" value={data.trades.toString()} />
      </div>
      {data.params && (
        <div className="mt-3 pt-3 border-t border-gray-700">
          <span className="text-xs text-gray-500">
            {Object.entries(data.params).map(([k, v]) => `${k}: ${v}`).join(' · ')}
          </span>
        </div>
      )}
    </div>
  );
}

function Metric({ label, value, positive, negative }: { label: string; value: string; positive?: boolean; negative?: boolean }) {
  let valueClass = 'text-gray-100';
  if (positive) valueClass = 'text-green-400';
  if (negative) valueClass = 'text-red-400';
  
  return (
    <div>
      <div className="text-xs text-gray-500">{label}</div>
      <div className={`text-lg font-semibold ${valueClass}`}>{value}</div>
    </div>
  );
}

export function SignalCard({ data }: { data: AnomalyResult }) {
  const typeColors: Record<string, string> = {
    spoofing: 'bg-red-900/50 border-red-700',
    absorption: 'bg-orange-900/50 border-orange-700',
    aggressive_flow: 'bg-yellow-900/50 border-yellow-700',
  };
  
  const colorClass = typeColors[data.type] || 'bg-gray-800 border-gray-700';
  
  return (
    <div className={`rounded-lg p-4 border ${colorClass}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium uppercase">{data.type}</span>
        <span className="text-xs bg-gray-800 px-2 py-1 rounded">
          {Math.round(data.confidence * 100)}% confidence
        </span>
      </div>
      <p className="text-sm text-gray-300 mb-2">{data.explanation}</p>
      <div className="flex gap-4 text-xs text-gray-500">
        <span>Price: {data.price_level}</span>
        <span>Side: {data.side}</span>
      </div>
    </div>
  );
}