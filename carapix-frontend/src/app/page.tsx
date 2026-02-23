import Image from "next/image";
import Link from "next/link";
import { supabase } from "@/lib/supabaseClient";

const FALLBACK_IMAGE = "https://dummyimage.com/600x600/0f172a/ffffff&text=Perfil";

async function fetchFollowers() {
  const { data, error } = await supabase
    .from("instagram_followers")
    .select(
      "id, username, file_path, gpt_score, gpt_verdict, gpt_summary, gpt_classification, gpt_alert, gpt_dm_hook, gpt_analyzed_at, analysis_status"
    )
    .order("gpt_analyzed_at", { ascending: false });

  if (error) {
    console.error(error);
    return [];
  }
  return data ?? [];
}

function formatScore(score: number | null) {
  if (score === null || score === undefined) return "–";
  return score % 1 === 0 ? score.toFixed(0) : score.toFixed(1);
}

const statusColors: Record<string, string> = {
  done: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
  pending: "bg-amber-500/20 text-amber-300 border-amber-500/40",
  error: "bg-rose-500/20 text-rose-300 border-rose-500/40",
};

function formatDate(date: string | null) {
  if (!date) return "–";
  return new Date(date).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default async function Home() {
  const followers = await fetchFollowers();
  const total = followers.length;
  const ready = followers.filter((f) => f.analysis_status === "done").length;
  const pending = followers.filter((f) => f.analysis_status === "pending").length;
  const errors = followers.filter((f) => f.analysis_status === "error").length;

  return (
    <div className="min-h-screen bg-[#05070A] text-white">
      <header className="border-b border-white/5 bg-black/30 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-white/60">
              Cara de Pix Radar
            </p>
            <h1 className="text-2xl font-semibold">CRM de Seguidores</h1>
          </div>
          <Link
            href="https://vercel.com/new"
            className="rounded-full border border-white/20 px-4 py-2 text-sm text-white/70 hover:border-white/60"
          >
            Deploy no Vercel
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        <section className="grid gap-4 md:grid-cols-4">
          {[
            { label: "Total", value: total, tone: "text-white" },
            { label: "Prontos", value: ready, tone: "text-emerald-300" },
            { label: "Pendentes", value: pending, tone: "text-amber-300" },
            { label: "Erros", value: errors, tone: "text-rose-300" },
          ].map((stat) => (
            <div
              key={stat.label}
              className="rounded-2xl border border-white/5 bg-white/5 p-4"
            >
              <p className="text-sm text-white/60">{stat.label}</p>
              <p className={`text-3xl font-semibold ${stat.tone}`}>{stat.value}</p>
            </div>
          ))}
        </section>

        <section className="mt-10 space-y-4">
          {followers.length === 0 && (
            <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-8 text-center text-white/70">
              Nenhum seguidor analisado ainda.
            </div>
          )}

          {followers.map((follower) => (
            <article
              key={follower.id}
              className="grid gap-6 rounded-3xl border border-white/5 bg-white/5 p-6 transition hover:border-white/20 md:grid-cols-[220px,1fr]"
            >
              <div className="overflow-hidden rounded-2xl bg-black/40">
                <Image
                  src={follower.file_path ?? FALLBACK_IMAGE}
                  alt={`@${follower.username}`}
                  width={400}
                  height={400}
                  className="h-full w-full object-cover"
                  unoptimized
                />
              </div>

              <div className="space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="text-sm uppercase tracking-[0.4em] text-white/50">
                      @{follower.username}
                    </p>
                    <p className="text-xl font-semibold text-white/90">
                      {follower.gpt_verdict ?? "Sem veredito"}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="rounded-full border border-white/20 px-3 py-1 text-sm text-white/70">
                      CRA {formatScore(follower.gpt_score)}/10
                    </span>
                    <span
                      className={`rounded-full border px-3 py-1 text-xs uppercase tracking-widest ${
                        statusColors[follower.analysis_status] || "border-white/20 text-white/60"
                      }`}
                    >
                      {follower.analysis_status ?? "sem status"}
                    </span>
                  </div>
                </div>

                <div className="space-y-2 text-sm text-white/80">
                  <p className="font-medium text-white/70">
                    Classificação: {follower.gpt_classification ?? "—"}
                  </p>
                  {follower.gpt_summary && (
                    <ul className="list-disc space-y-1 pl-5 text-white/70">
                      {follower.gpt_summary.split("\n").map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  )}
                  {follower.gpt_alert && (
                    <p className="text-rose-300">⚠️ {follower.gpt_alert}</p>
                  )}
                </div>

                {follower.gpt_dm_hook && (
                  <div className="rounded-2xl border border-white/10 bg-black/40 p-4 text-sm text-white/80">
                    <p className="text-xs uppercase tracking-[0.3em] text-white/40">
                      Mensagem inicial sugerida
                    </p>
                    <p>{follower.gpt_dm_hook}</p>
                  </div>
                )}

                <p className="text-xs text-white/50">
                  Atualizado em {formatDate(follower.gpt_analyzed_at)}
                </p>
              </div>
            </article>
          ))}
        </section>
      </main>
    </div>
  );
}
