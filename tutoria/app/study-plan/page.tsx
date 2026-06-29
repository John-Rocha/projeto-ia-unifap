"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, StudyPlanResponse } from "@/lib/api";

export default function StudyPlanPage() {
  return (
    <Suspense>
      <StudyPlanInner />
    </Suspense>
  );
}

function StudyPlanInner() {
  const searchParams = useSearchParams();
  const weaknesses = searchParams.getAll("w");

  const [plan, setPlan] = useState<StudyPlanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (weaknesses.length === 0) {
      setError("Nenhuma fraqueza identificada. Faça um quiz diagnóstico primeiro.");
      setLoading(false);
      return;
    }

    api
      .studyPlan(weaknesses)
      .then((data) => {
        setPlan(data);
      })
      .catch(() => {
        setError("Erro ao gerar plano de estudos. Tente novamente.");
      })
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-3 text-slate-500">
        <div className="w-8 h-8 border-2 border-indigo-300 border-t-indigo-600 rounded-full animate-spin" />
        <p>Gerando plano de estudos personalizado…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">{error}</div>
        <a href="/" className="block mt-4 text-sm text-indigo-600 hover:underline">
          ← Voltar às aulas
        </a>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 flex flex-col gap-6">
      <div>
        <a href="/" className="text-sm text-indigo-600 hover:underline">← Voltar às aulas</a>
        <h1 className="text-xl font-bold text-slate-800 mt-2">{plan?.title}</h1>
        {weaknesses.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {weaknesses.map((w) => (
              <span key={w} className="text-xs rounded-full bg-amber-100 text-amber-800 px-2.5 py-0.5">
                {w}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="flex flex-col gap-4">
        {plan?.steps.map((step) => (
          <div key={step.order} className="bg-white rounded-xl border border-slate-200 p-5 flex gap-4">
            <span className="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center">
              {step.order}
            </span>
            <div className="flex flex-col gap-1">
              <h2 className="font-semibold text-slate-800">{step.topic}</h2>
              <p className="text-sm text-slate-600">{step.description}</p>
              <p className="text-xs text-indigo-500 font-medium mt-1">{step.source}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-3">
        <a
          href="/chat"
          className="flex-1 text-center rounded-lg bg-indigo-600 text-white font-medium py-2.5 hover:bg-indigo-700 transition-colors"
        >
          Perguntar ao tutor →
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
