export function cn(...inputs: (string | undefined | null | false)[]): string {
  return inputs.filter(Boolean).join(" ");
}

export type ResponseType = "text" | "backtest" | "anomaly" | "unknown";

export interface ParsedResponse {
  type: ResponseType;
  content?: string;
  backtest?: BacktestData;
  anomaly?: AnomalyData;
}

export interface BacktestData {
  symbol: string;
  strategy: string;
  params: Record<string, number>;
  pnl: number;
  sharpe: number;
  max_drawdown: number;
  trades: number;
}

export interface AnomalyData {
  type: "spoofing" | "absorption" | "aggressive_flow";
  confidence: number;
  side: string;
  price_level: number;
  explanation: string;
  metrics: Record<string, number>;
}

export function parseResponse(response: string | unknown): ParsedResponse {
  if (!response || typeof response === "string") {
    try {
      const parsed = JSON.parse(response as string);
      return parseJsonResponse(parsed);
    } catch {
      return { type: "text", content: response as string };
    }
  }

  if (typeof response === "object") {
    return parseJsonResponse(response);
  }

  return { type: "text", content: String(response) };
}

function parseJsonResponse(data: unknown): ParsedResponse {
  if (!data || typeof data !== "object") {
    return { type: "text", content: String(data) };
  }

  const obj = data as Record<string, unknown>;

  // Check if backtest result (has pnl)
  if ("pnl" in obj && "strategy" in obj && "symbol" in obj) {
    return {
      type: "backtest",
      backtest: obj as unknown as BacktestData,
    };
  }

  // Check if anomaly
  if (obj.data && Array.isArray(obj.data) && obj.data.length > 0) {
    const firstItem = obj.data[0] as Record<string, unknown>;
    if ("type" in firstItem && ["spoofing", "absorption", "aggressive_flow"].includes(firstItem.type as string)) {
      return {
        type: "anomaly",
        anomaly: firstItem as unknown as AnomalyData,
      };
    }
  }

  // Check direct anomaly
  if ("type" in obj && ["spoofing", "absorption", "aggressive_flow"].includes(obj.type as string)) {
    return {
      type: "anomaly",
      anomaly: obj as unknown as AnomalyData,
    };
  }

  // Default to text
  const content = obj.response || obj.content || obj.message || JSON.stringify(obj);
  return { type: "text", content: typeof content === "string" ? content : String(content) };
}