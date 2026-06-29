import { api, Topic } from "@/lib/api";

export const revalidate = 3600;

function TopicCard({ topic, index }: { topic: Topic; index: number }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 flex flex-col gap-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <span className="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 text-sm font-bold flex items-center justify-center">
          {String(index + 1).padStart(2, "0")}
        </span>
        <div>
          <h2 className="font-semibold text-slate-800">{topic.title}</h2>
          <p className="text-sm text-slate-500 mt-0.5">{topic.description}</p>
        </div>
      </div>
      <div className="flex gap-2 mt-auto">
        <a
          href={`/diagnostic/${topic.id}`}
          className="flex-1 text-center text-sm font-medium py-2 rounded-lg border border-indigo-200 text-indigo-600 hover:bg-indigo-50 transition-colors"
        >
          Quiz diagnóstico
        </a>
        <a
          href={`/chat?topic=${topic.id}`}
          className="flex-1 text-center text-sm font-medium py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
        >
          Perguntar ao tutor
        </a>
      </div>
    </div>
  );
}

export default async function HomePage() {
  let topics: Topic[] = [];
  try {
    const data = await api.topics();
    topics = data.topics;
  } catch {
    // backend offline — show empty state
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-800">Aulas da Disciplina</h1>
        <p className="text-slate-500 mt-1">
          Escolha uma aula para fazer o quiz diagnóstico ou conversar com o tutor.
        </p>
      </div>

      {topics.length === 0 ? (
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-6 text-center text-amber-800">
          Não foi possível carregar as aulas. Verifique se o backend está rodando.
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {topics.map((t, i) => (
            <TopicCard key={t.id} topic={t} index={i} />
          ))}
        </div>
      )}

      <div className="mt-10 rounded-xl bg-indigo-600 p-6 text-white flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h2 className="font-semibold text-lg">Precisa de ajuda geral?</h2>
          <p className="text-indigo-200 text-sm mt-0.5">Converse com o tutor sem filtro de aula.</p>
        </div>
        <a
          href="/chat"
          className="flex-shrink-0 rounded-lg bg-white text-indigo-600 font-medium px-5 py-2.5 hover:bg-indigo-50 transition-colors"
        >
          Abrir chat →
        </a>
      </div>
    </div>
  );
}
