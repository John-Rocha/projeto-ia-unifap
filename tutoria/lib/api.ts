const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

// Types
export interface Topic {
  id: string;
  title: string;
  description: string;
}

export interface DiagnosticQuestion {
  id: string;
  question: string;
  options: string[];
}

export interface DiagnosticQuizResponse {
  topic_id: string;
  title: string;
  questions: DiagnosticQuestion[];
}

export interface DiagnosticResult {
  score: number;
  total: number;
  weaknesses: string[];
  recommendation: string;
}

export interface Source {
  aula?: string;
  titulo_aula?: string;
  tema?: string;
  topico?: string;
  pagina?: number;
  score?: number;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  retrieved_chunks: string[];
  confidence: number | null;
}

export interface StudyStep {
  order: number;
  topic: string;
  description: string;
  source: string;
}

export interface StudyPlanResponse {
  title: string;
  steps: StudyStep[];
}

// API calls
export const api = {
  topics(): Promise<{ topics: Topic[] }> {
    return get("/topics");
  },

  getQuiz(topicId: string): Promise<DiagnosticQuizResponse> {
    return get(`/diagnostic/quiz?topic_id=${topicId}`);
  },

  submitQuiz(topicId: string, answers: { question_id: string; selected_option: string }[]): Promise<DiagnosticResult> {
    return post("/diagnostic/submit", { topic_id: topicId, answers });
  },

  chat(question: string, topicId?: string): Promise<ChatResponse> {
    return post("/chat", { question, topic_id: topicId ?? null, top_k: 5 });
  },

  studyPlan(weaknesses: string[], goal = "Revisar para a prova"): Promise<StudyPlanResponse> {
    return post("/study-plan", { weaknesses, goal });
  },
};
