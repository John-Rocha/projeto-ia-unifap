"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api, DiagnosticQuestion, DiagnosticResult } from "@/lib/api";

type Phase = "loading" | "error" | "quiz" | "result";

export default function DiagnosticPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();

  const [phase, setPhase] = useState<Phase>("loading");
  const [title, setTitle] = useState("");
  const [questions, setQuestions] = useState<DiagnosticQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<DiagnosticResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .getQuiz(id)
      .then((data) => {
        setTitle(data.title);
        setQuestions(data.questions);
        setPhase("quiz");
      })
      .catch(() => {
        setError("Não foi possível carregar o quiz. Verifique se o backend está rodando.");
        setPhase("error");
      });
  }, [id]);

  async function handleSubmit() {
    if (Object.keys(answers).length < questions.length) {
      setError("Responda todas as questões antes de enviar.");
      return;
    }
    setError("");
    setSubmitting(true);
    try {
      const answerList = Object.entries(answers).map(([question_id, selected_option]) => ({
        question_id,
        selected_option,
      }));
      const res = await api.submitQuiz(id, answerList);
      setResult(res);
      setPhase("result");
    } catch {
      setError("Erro ao enviar respostas. Tente novamente.");
    } finally {
      setSubmitting(false);
    }
  }

  function goToStudyPlan() {
    if (!result) return;
    const params = new URLSearchParams();
    result.weaknesses.forEach((w) => params.append("w", w));
    router.push(`/study-plan?${params.toString()}`);
  }

  if (phase === "loading") {
    return (
      <div className="flex items-center justify-center py-32 text-slate-500">
        Carregando quiz…
      </div>
    );
  }

  if (phase === "error") {
    return (
      <div className="mx-auto max-w-2xl px-4 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">{error}</div>
      </div>
    );
  }

  if (phase === "result" && result) {
    const pct = Math.round((result.score / result.total) * 100);
    const color = pct >= 70 ? "text-green-600" : pct >= 40 ? "text-amber-600" : "text-red-600";

    return (
      <div className="mx-auto max-w-2xl px-4 py-10 flex flex-col gap-6">
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h1 className="text-xl font-bold text-slate-800 mb-1">Resultado do Quiz</h1>
          <p className="text-slate-500 text-sm">{title}</p>

          <div className="mt-6 flex items-center gap-4">
            <span className={`text-5xl font-bold ${color}`}>{pct}%</span>
            <div>
              <p className="text-slate-700 font-medium">{result.score} de {result.total} questões corretas</p>
              <p className="text-slate-500 text-sm mt-0.5">{result.recommendation}</p>
            </div>
          </div>
        </div>

        {result.weaknesses.length > 0 && (
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h2 className="font-semibold text-slate-800 mb-3">Pontos a reforçar</h2>
            <ul className="flex flex-wrap gap-2">
              {result.weaknesses.map((w) => (
                <li
                  key={w}
                  className="rounded-full bg-amber-100 text-amber-800 text-sm px-3 py-1"
                >
                  {w}
                </li>
              ))}
            </ul>
            <button
              onClick={goToStudyPlan}
              className="mt-4 w-full rounded-lg bg-indigo-600 text-white font-medium py-2.5 hover:bg-indigo-700 transition-colors"
            >
              Gerar plano de estudos personalizado →
            </button>
          </div>
        )}

        <div className="flex gap-3">
          <a
            href={`/chat?topic=${id}`}
            className="flex-1 text-center rounded-lg border border-indigo-200 text-indigo-600 font-medium py-2.5 hover:bg-indigo-50 transition-colors"
          >
            Perguntar ao tutor sobre esta aula
          </a>
          <a
            href="/"
            className="flex-1 text-center rounded-lg border border-slate-200 text-slate-600 font-medium py-2.5 hover:bg-slate-50 transition-colors"
          >
            Voltar às aulas
          </a>
        </div>
      </div>
    );
  }

  // Quiz phase
  return (
    <div className="mx-auto max-w-2xl px-4 py-10 flex flex-col gap-6">
      <div>
        <a href="/" className="text-sm text-indigo-600 hover:underline">← Voltar às aulas</a>
        <h1 className="text-xl font-bold text-slate-800 mt-2">{title}</h1>
        <p className="text-slate-500 text-sm">{questions.length} questões</p>
      </div>

      {questions.map((q, qi) => (
        <div key={q.id} className="bg-white rounded-xl border border-slate-200 p-5">
          <p className="font-medium text-slate-800 mb-4">
            <span className="text-indigo-500 mr-2">{qi + 1}.</span>
            {q.question}
          </p>
          <div className="flex flex-col gap-2">
            {q.options.map((opt) => {
              const selected = answers[q.id] === opt;
              return (
                <button
                  key={opt}
                  onClick={() => setAnswers((prev) => ({ ...prev, [q.id]: opt }))}
                  className={`text-left rounded-lg border px-4 py-3 text-sm transition-colors ${
                    selected
                      ? "border-indigo-500 bg-indigo-50 text-indigo-800"
                      : "border-slate-200 text-slate-700 hover:border-indigo-300 hover:bg-slate-50"
                  }`}
                >
                  {opt}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">{error}</p>
      )}

      <button
        onClick={handleSubmit}
        disabled={submitting}
        className="w-full rounded-lg bg-indigo-600 text-white font-medium py-3 hover:bg-indigo-700 disabled:opacity-50 transition-colors"
      >
        {submitting ? "Enviando…" : "Enviar respostas"}
      </button>
    </div>
  );
}
