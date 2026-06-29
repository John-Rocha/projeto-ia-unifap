"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, Source, Topic } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  confidence?: number | null;
}

export default function ChatPage() {
  return (
    <Suspense>
      <ChatInner />
    </Suspense>
  );
}

function ChatInner() {
  const searchParams = useSearchParams();
  const initialTopic = searchParams.get("topic") ?? "";

  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState(initialTopic);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.topics().then((d) => setTopics(d.topics)).catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend() {
    const q = input.trim();
    if (!q || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: q }]);
    setInput("");
    setLoading(true);

    try {
      const res = await api.chat(q, selectedTopic || undefined);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.answer,
          sources: res.sources,
          confidence: res.confidence,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Erro ao contatar o tutor. Tente novamente." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 flex flex-col" style={{ height: "calc(100vh - 120px)" }}>
      {/* Topic filter */}
      <div className="mb-4 flex items-center gap-3">
        <label className="text-sm font-medium text-slate-600 flex-shrink-0">Filtrar por aula:</label>
        <select
          value={selectedTopic}
          onChange={(e) => setSelectedTopic(e.target.value)}
          className="text-sm border border-slate-200 rounded-lg px-3 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
        >
          <option value="">Todas as aulas</option>
          {topics.map((t) => (
            <option key={t.id} value={t.id}>
              {t.title}
            </option>
          ))}
        </select>
        {selectedTopic && (
          <button
            onClick={() => setSelectedTopic("")}
            className="text-xs text-slate-400 hover:text-slate-600"
          >
            ✕ limpar
          </button>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-1">
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-center py-16 text-slate-400">
            <span className="text-4xl mb-3">🤖</span>
            <p className="font-medium text-slate-500">Olá! Sou o TutorIA.</p>
            <p className="text-sm mt-1">Faça uma pergunta sobre o conteúdo da disciplina.</p>
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-indigo-600 text-white rounded-br-sm"
                  : "bg-white border border-slate-200 text-slate-800 rounded-bl-sm"
              }`}
            >
              <p className="whitespace-pre-wrap">{m.content}</p>

              {m.sources && m.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-100">
                  <p className="text-xs text-slate-400 font-medium mb-1">Fontes</p>
                  <div className="flex flex-col gap-1">
                    {m.sources.slice(0, 3).map((s, si) => (
                      <span key={si} className="text-xs text-slate-500">
                        {s.titulo_aula ?? s.aula}
                        {s.pagina ? ` · p.${s.pagina}` : ""}
                        {s.score ? ` · ${(s.score * 100).toFixed(0)}%` : ""}
                      </span>
                    ))}
                  </div>
                  {m.confidence != null && (
                    <p className="text-xs text-slate-400 mt-1">
                      Confiança: {(m.confidence * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-sm px-4 py-3">
              <div className="flex gap-1 items-center">
                <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="mt-4 flex gap-2 bg-white border border-slate-200 rounded-xl p-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Digite sua pergunta… (Enter para enviar)"
          rows={1}
          className="flex-1 resize-none bg-transparent text-sm text-slate-800 placeholder-slate-400 focus:outline-none px-2 py-1"
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="flex-shrink-0 rounded-lg bg-indigo-600 text-white px-4 py-2 text-sm font-medium hover:bg-indigo-700 disabled:opacity-40 transition-colors"
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
