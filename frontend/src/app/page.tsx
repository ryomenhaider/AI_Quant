import { Chat } from "@/components/chat/Chat";
import { BarChart3 } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-slate-100">
      <div className="max-w-5xl mx-auto h-screen flex flex-col">
        <header className="border-b border-slate-800 px-4 py-3 flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-lg">
            <BarChart3 className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold">AI Quant Analyst</h1>
            <p className="text-xs text-slate-500">Real-time market intelligence</p>
          </div>
        </header>

        <main className="flex-1 overflow-hidden">
          <Chat />
        </main>
      </div>
    </div>
  );
}