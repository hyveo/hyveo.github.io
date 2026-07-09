import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Sun, Moon } from "lucide-react";

const PROJECTS = [
  {
    name: "daily-ai-insight",
    lang: "JavaScript",
    langColor: "#F1E05A",
    stars: 31,
    desc: "YouTube 방송 콘텐츠를 AI 분석 리포트로 재구성해 핵심 주제와 관전 포인트를 빠르게 읽을 수 있게 정리합니다.",
    tags: ["ai", "youtube", "report"],
    status: "active",
    commits: 64,
    lastCommit: "오늘",
    url: "https://hyveo.github.io/daily-ai-insight/",
  },
  {
    name: "birthday-color-palatte",
    lang: "JavaScript",
    langColor: "#F1E05A",
    stars: 18,
    desc: "생일을 입력하면 나만의 Birthday Color chip을 보여주는 모바일 중심의 컬러 제너레이터입니다.",
    tags: ["color", "birthday", "mobile"],
    status: "active",
    commits: 42,
    lastCommit: "오늘",
    url: "https://hyveo.github.io/birthday-color-palatte/",
  },
  {
    name: "today-receipt",
    lang: "JavaScript",
    langColor: "#F1E05A",
    stars: 12,
    desc: "하루 지출을 영수증처럼 기록하고, localStorage 저장과 PNG 내보내기를 지원하는 미니멀 웹 도구입니다.",
    tags: ["receipt", "localStorage", "png"],
    status: "active",
    commits: 28,
    lastCommit: "오늘",
    url: "https://hyveo.github.io/today-receipt/",
  },
  {
    name: "wedding-invitation-card",
    lang: "TypeScript",
    langColor: "#3178C6",
    stars: 7,
    desc: "모바일에서 보기 좋은 청첩장 카드를 만들고, 공유하기 쉽게 다듬는 작업 중인 프로젝트입니다.",
    tags: ["wedding", "mobile", "card"],
    status: "wip",
    commits: 12,
    lastCommit: "작업 중",
    url: "",
  },
];

const STACK = [
  { name: "React", color: "#61DAFB" },
  { name: "TypeScript", color: "#3178C6" },
  { name: "Next.js", color: "#E6EDF3" },
  { name: "Supabase", color: "#3ECF8E" },
  { name: "Rust", color: "#FF4E00" },
  { name: "Tailwind", color: "#38BDF8" },
  { name: "Prisma", color: "#5A67D8" },
  { name: "Figma", color: "#F24E1E" },
];

const COMMITS = [
  { hash: "a3f8c21", msg: "feat: 씨앗 성장 애니메이션 추가", time: "2h ago" },
  { hash: "b19de04", msg: "fix: 모바일에서 레이아웃 깨지는 거 고침", time: "1d ago" },
  { hash: "c72af15", msg: "chore: 의존성 업데이트", time: "2d ago" },
  { hash: "d45bc30", msg: "feat: 이메일 예약 발송 기능 구현 완료!!", time: "3d ago" },
  { hash: "e88fd02", msg: "refactor: 컴포넌트 분리", time: "4d ago" },
];

function Terminal({ lines }: { lines: string[] }) {
  const [displayed, setDisplayed] = useState<string[]>([]);
  const [cursor, setCursor] = useState(true);

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      if (i < lines.length) {
        setDisplayed((prev) => [...prev, lines[i]]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 600);
    const blink = setInterval(() => setCursor((c) => !c), 500);
    return () => { clearInterval(interval); clearInterval(blink); };
  }, []);

  return (
    <div className="bg-[#0D1117] rounded-lg border border-white/10 overflow-hidden font-mono text-sm">
      <div className="flex items-center gap-2 px-4 py-2.5 bg-white/5 border-b border-white/10">
        <div className="w-3 h-3 rounded-full bg-[#F85149]" />
        <div className="w-3 h-3 rounded-full bg-[#F0A732]" />
        <div className="w-3 h-3 rounded-full bg-[#39D353]" />
        <span className="ml-2 text-[#7D8590] text-xs">~/projects</span>
      </div>
      <div className="p-4 space-y-1 min-h-[120px]">
        {displayed.map((line, i) => (
          <div key={i} className="flex gap-2">
            <span className="text-[#39D353] select-none">❯</span>
            <span className="text-[#E6EDF3]">{line}</span>
          </div>
        ))}
        {displayed.length < lines.length && (
          <div className="flex gap-2">
            <span className="text-[#39D353] select-none">❯</span>
            <span className={`w-2 h-4 bg-[#E6EDF3] inline-block ${cursor ? "opacity-100" : "opacity-0"}`} />
          </div>
        )}
      </div>
    </div>
  );
}

function getYearProgress() {
  const days = 7;
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const start = new Date(today.getFullYear(), 0, 1);
  const elapsedDays = Math.floor((today.getTime() - start.getTime()) / 86400000) + 1;
  const weeks = Math.ceil(elapsedDays / days);
  const levels = [1, 1, 2, 0, 2, 3, 1, 4, 2, 0, 3, 2, 1, 4];
  const colors = ["#161B22", "#0e4429", "#006d32", "#26a641", "#39d353"];
  const cells = Array.from({ length: weeks * days }).map((_, index) => {
    const hasDate = index < elapsedDays;
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    const level = hasDate ? levels[(index + date.getMonth() + date.getDay()) % levels.length] : 0;

    return {
      hasDate,
      count: level * 3,
      color: colors[level],
      label: hasDate
        ? date.toLocaleDateString("ko-KR", { month: "long", day: "numeric" })
        : "",
    };
  });

  return {
    cells,
    elapsedDays,
    weeks,
    days,
  };
}

function ContribGrid({ progress }: { progress: ReturnType<typeof getYearProgress> }) {
  const { cells, elapsedDays, weeks, days } = progress;
  const fillOrder = useMemo(() => {
    const todayIndex = elapsedDays - 1;
    const order: number[] = [];

    for (let week = 0; week < weeks; week++) {
      const start = week * days;
      const end = Math.min(start + days, elapsedDays);
      const weekIndexes = Array.from({ length: end - start })
        .map((_, index) => start + index)
        .filter((index) => index !== todayIndex);

      for (let i = weekIndexes.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [weekIndexes[i], weekIndexes[j]] = [weekIndexes[j], weekIndexes[i]];
      }

      order.push(...weekIndexes);
    }

    if (todayIndex >= 0) order.push(todayIndex);

    return order;
  }, [days, elapsedDays, weeks]);
  const [filledIndexes, setFilledIndexes] = useState<Set<number>>(new Set());
  const [currentIndex, setCurrentIndex] = useState<number | null>(null);

  useEffect(() => {
    if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) {
      setFilledIndexes(new Set(fillOrder));
      setCurrentIndex(null);
      return;
    }

    let index = 0;
    let timeout = 0;
    setFilledIndexes(new Set());
    setCurrentIndex(null);

    function fillNext() {
      if (index >= fillOrder.length) return;

      const nextIndex = fillOrder[index];
      setFilledIndexes((filled) => {
        const next = new Set(filled);
        next.add(nextIndex);
        return next;
      });
      setCurrentIndex(nextIndex);
      index += 1;

      if (index < fillOrder.length) {
        timeout = window.setTimeout(fillNext, 30 + Math.random() * 130);
      }
    }

    timeout = window.setTimeout(fillNext, 120);

    return () => window.clearTimeout(timeout);
  }, [fillOrder]);

  return (
    <div className="flex gap-1">
      {Array.from({ length: weeks }).map((_, w) => (
        <div key={w} className="flex flex-col gap-1">
          {Array.from({ length: days }).map((_, d) => {
            const index = w * days + d;
            const cell = cells[index];
            const isFilled = cell.hasDate && filledIndexes.has(index);
            const isCurrent = index === currentIndex;
            return (
              <div
                key={d}
                className={`w-3 h-3 rounded-sm transition-all duration-150 ${
                  isCurrent ? "animate-pulse ring-2 ring-primary/40" : ""
                }`}
                style={{
                  backgroundColor: isFilled ? cell.color : "#E6EDF3",
                  opacity: cell.hasDate ? (isFilled ? 1 : 0.55) : 0.18,
                  transform: cell.hasDate && isFilled ? "scale(1)" : "scale(0.82)",
                }}
                title={cell.hasDate ? `${cell.label}: ${cell.count} contributions` : ""}
              />
            );
          })}
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState<"all" | "active" | "wip">("all");
  const [copiedEmail, setCopiedEmail] = useState(false);
  const [dark, setDark] = useState(false);
  const contributionProgress = getYearProgress();

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const filtered = PROJECTS.filter((p) => activeTab === "all" || p.status === activeTab);

  const handleCopy = () => {
    navigator.clipboard.writeText("app.hyveo@gmail.com");
    setCopiedEmail(true);
    setTimeout(() => setCopiedEmail(false), 2000);
  };

  return (
    <div
      className="min-h-screen bg-background text-foreground"
      style={{ fontFamily: "'Inter', sans-serif" }}
    >
      {/* NAV */}
      <nav className="border-b border-border sticky top-0 z-50 bg-background/80 backdrop-blur-md">
        <div className="max-w-4xl mx-auto px-6 py-3 flex items-center justify-between">
          <span style={{ fontFamily: "'JetBrains Mono', monospace" }} className="text-sm text-primary font-bold">
            ~/hyveo
          </span>
          <div className="flex items-center gap-6">
            <a href="#projects" className="text-xs text-muted-foreground hover:text-foreground transition-colors" style={{ fontFamily: "'JetBrains Mono', monospace" }}>projects</a>
            <a href="#about" className="text-xs text-muted-foreground hover:text-foreground transition-colors" style={{ fontFamily: "'JetBrains Mono', monospace" }}>about</a>
            <button
              onClick={() => setDark((d) => !d)}
              className="p-1.5 rounded border border-border text-muted-foreground hover:text-foreground hover:border-foreground/30 transition-all"
              aria-label="Toggle theme"
            >
              <AnimatePresence mode="wait" initial={false}>
                <motion.div
                  key={dark ? "sun" : "moon"}
                  initial={{ opacity: 0, rotate: -30, scale: 0.8 }}
                  animate={{ opacity: 1, rotate: 0, scale: 1 }}
                  exit={{ opacity: 0, rotate: 30, scale: 0.8 }}
                  transition={{ duration: 0.15 }}
                >
                  {dark ? <Sun size={14} /> : <Moon size={14} />}
                </motion.div>
              </AnimatePresence>
            </button>
            <button
              onClick={handleCopy}
              className="text-xs bg-primary text-primary-foreground px-4 py-1.5 rounded font-bold hover:opacity-90 transition-opacity"
              style={{ fontFamily: "'JetBrains Mono', monospace" }}
            >
              {copiedEmail ? "copied!" : "contact"}
            </button>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="max-w-4xl mx-auto px-6 pt-16 pb-12">
        <div className="grid md:grid-cols-2 gap-12 items-start">
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            {/* status badge */}
            <div className="flex items-center gap-2 mb-6">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />
              </span>
              <span className="text-xs text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                available for collaboration
              </span>
            </div>

            <div style={{ fontFamily: "'JetBrains Mono', monospace" }} className="text-muted-foreground text-sm mb-2">
              <span className="text-accent">const</span>{" "}
              <span className="text-[#F97316]">me</span>{" "}
              <span className="text-foreground">= {"{"}</span>
            </div>

            <h1 className="text-4xl md:text-5xl font-bold text-foreground leading-tight mb-1 pl-4">
              토이 메이커,<br />
              <span className="text-primary">코딩</span>이 취미인
            </h1>

            <div style={{ fontFamily: "'JetBrains Mono', monospace" }} className="text-muted-foreground text-sm mt-2">
              <span className="text-foreground">{"}"}</span>
            </div>

            <p className="mt-6 text-[#7D8590] text-sm leading-relaxed max-w-xs">
              필요해서 만들고, 재밌어서 계속하는 개발자예요.
              작고 쓸모있는 것들을 좋아해요 🌱
            </p>

            <div className="mt-6 flex gap-3">
              <a
                href="#projects"
                className="bg-primary text-primary-foreground text-xs px-5 py-2 rounded font-bold hover:opacity-90 transition-all"
                style={{ fontFamily: "'JetBrains Mono', monospace" }}
              >
                view projects →
              </a>
              <a
                href="https://github.com/hyveo"
                className="border border-border text-foreground text-xs px-5 py-2 rounded font-bold hover:border-primary transition-all"
                style={{ fontFamily: "'JetBrains Mono', monospace" }}
              >
                github ↗
              </a>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Terminal
              lines={[
                "ls -la ./projects",
                "git log --oneline -5",
                "npm run dev",
                "Listening on http://localhost:3000 ✓",
              ]}
            />

            {/* commit feed */}
            <div className="mt-3 bg-card border border-border rounded-lg overflow-hidden">
              <div className="px-4 py-2.5 border-b border-border flex items-center gap-2">
                <span className="text-xs text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                  recent commits
                </span>
              </div>
              <div className="divide-y divide-border">
                {COMMITS.slice(0, 3).map((c) => (
                  <div key={c.hash} className="px-4 py-2.5 flex items-center gap-3 hover:bg-white/5 transition-colors group">
                    <span
                      className="text-[10px] text-accent shrink-0"
                      style={{ fontFamily: "'JetBrains Mono', monospace" }}
                    >
                      {c.hash}
                    </span>
                    <span className="text-xs text-foreground flex-1 truncate">{c.msg}</span>
                    <span className="text-[10px] text-muted-foreground shrink-0">{c.time}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* contrib graph */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 bg-card border border-border rounded-lg p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
              contributions this year
            </span>
            <span className="text-xs text-primary font-bold" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
              {contributionProgress.elapsedDays} total
            </span>
          </div>
          <div className="overflow-x-auto">
            <ContribGrid progress={contributionProgress} />
          </div>
        </motion.div>
      </section>

      {/* PROJECTS */}
      <section id="projects" className="max-w-4xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-bold text-foreground text-lg">
            <span className="text-muted-foreground text-sm mr-2" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
              ~/projects
            </span>
          </h2>
          <div className="flex gap-1 border border-border rounded-md overflow-hidden" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
            {(["all", "active", "wip"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`text-xs px-3 py-1.5 transition-colors ${
                  activeTab === tab
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>

        <AnimatePresence mode="popLayout">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {filtered.map((project) => (
              <motion.a
                key={project.name}
                href={project.url || undefined}
                target={project.url ? "_blank" : undefined}
                rel={project.url ? "noreferrer" : undefined}
                layout
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.96 }}
                transition={{ duration: 0.2 }}
                className={`bg-card border border-border rounded-lg p-5 hover:border-white/20 transition-all group block no-underline text-inherit ${
                  project.url ? "cursor-pointer" : "cursor-default"
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span
                      className="text-accent font-bold text-sm"
                      style={{ fontFamily: "'JetBrains Mono', monospace" }}
                    >
                      {project.name}
                    </span>
                    {project.status === "wip" && (
                      <span className="text-[10px] border border-[#F0A732] text-[#F0A732] px-1.5 py-0.5 rounded-sm" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                        wip
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.872 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z" />
                    </svg>
                    <span className="text-xs">{project.stars}</span>
                  </div>
                </div>

                <p className="text-[#7D8590] text-xs leading-relaxed mb-4">{project.desc}</p>

                <div className="flex items-center gap-3 flex-wrap">
                  <div className="flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: project.langColor }} />
                    <span className="text-xs text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                      {project.lang}
                    </span>
                  </div>
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] bg-white/5 text-muted-foreground px-2 py-0.5 rounded-full"
                      style={{ fontFamily: "'JetBrains Mono', monospace" }}
                    >
                      #{tag}
                    </span>
                  ))}
                </div>

                <div className="mt-3 pt-3 border-t border-border flex items-center justify-between">
                  <span className="text-[10px] text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                    {project.commits} commits
                  </span>
                  <span className="text-[10px] text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                    updated {project.lastCommit}
                  </span>
                </div>
              </motion.a>
            ))}
          </div>
        </AnimatePresence>
      </section>

      {/* ABOUT */}
      <section id="about" className="max-w-4xl mx-auto px-6 py-12">
        <div className="bg-card border border-border rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-border flex items-center gap-2">
            <span className="text-muted-foreground text-xs" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
              README.md
            </span>
          </div>
          <div className="p-6 grid md:grid-cols-5 gap-8">
            <div className="md:col-span-3 space-y-4">
              <div>
                <h2 className="text-xl font-bold text-foreground mb-1">안녕하세요, 저는 hyveo예요 👋</h2>
                <p className="text-muted-foreground text-sm">
                  <span className="text-primary" style={{ fontFamily: "'JetBrains Mono', monospace" }}>// </span>
                  full-stack developer & weekend tinkerer
                </p>
              </div>

              <div className="text-sm text-[#7D8590] leading-relaxed space-y-2">
                <p>
                  코딩을 일로도 하고 취미로도 해요. 퇴근 후 노트북 열고
                  "이거 있으면 편하겠다" 싶은 것들을 만드는 게 낙이에요.
                </p>
                <p>
                  완벽한 제품보다 작동하는 것, 큰 서비스보다 내 생활에
                  딱 맞는 것을 좋아해요. 코드보다 사람이 먼저인 개발자가
                  되고 싶어요.
                </p>
              </div>

              <div className="pt-2">
                <p className="text-xs text-muted-foreground mb-3" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                  {">"} tech stack
                </p>
                <div className="flex flex-wrap gap-2">
                  {STACK.map((s) => (
                    <span
                      key={s.name}
                      className="text-xs border border-border px-2.5 py-1 rounded-full hover:border-white/30 transition-colors cursor-default"
                      style={{ color: s.color, fontFamily: "'JetBrains Mono', monospace" }}
                    >
                      {s.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="md:col-span-2 space-y-3">
              <div className="bg-background rounded-lg border border-border p-4 space-y-2.5">
                {[
                  { key: "location", val: "Seoul, KR 🇰🇷" },
                  { key: "work", val: "개발자 @ dayjob" },
                  { key: "side_hustle", val: "indie maker" },
                  { key: "status", val: "☕ brewing" },
                ].map(({ key, val }) => (
                  <div key={key} className="flex gap-2 text-xs" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                    <span className="text-[#F97316] shrink-0">{key}:</span>
                    <span className="text-foreground">{val}</span>
                  </div>
                ))}
              </div>

              <div className="bg-background rounded-lg border border-border p-4">
                <p className="text-xs text-muted-foreground mb-2" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                  {">"} git log --author="me" --format="%s"
                </p>
                <div className="space-y-1.5 max-h-[120px] overflow-y-auto">
                  {COMMITS.map((c) => (
                    <div key={c.hash} className="text-[11px] text-[#7D8590] truncate">
                      <span className="text-accent mr-1" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
                        {c.hash}
                      </span>
                      {c.msg}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-4xl mx-auto px-6 py-12">
        <div className="border border-dashed border-border rounded-lg p-8 text-center">
          <p className="text-muted-foreground text-xs mb-2" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
            {"> "}echo "같이 뭔가 만들어 볼래요?"
          </p>
          <h2 className="text-xl font-bold text-foreground mb-2">
            피드백이든 협업 제안이든 환영해요
          </h2>
          <p className="text-muted-foreground text-sm mb-6">
            버그 제보, 기능 제안, 아니면 그냥 안녕 인사도 좋아요 :)
          </p>
          <div className="flex justify-center gap-3 flex-wrap">
            <button
              onClick={handleCopy}
              className="bg-primary text-primary-foreground text-xs px-6 py-2.5 rounded font-bold hover:opacity-90 transition-opacity"
              style={{ fontFamily: "'JetBrains Mono', monospace" }}
            >
              {copiedEmail ? "✓ copied!" : "copy email"}
            </button>
            <a
              href="https://github.com/hyveo"
              className="border border-border text-foreground text-xs px-6 py-2.5 rounded font-bold hover:border-white/30 transition-colors"
              style={{ fontFamily: "'JetBrains Mono', monospace" }}
            >
              open issue ↗
            </a>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-border py-6">
        <div className="max-w-4xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-3">
          <span className="text-xs text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
            ~/hyveo — built with ☕ & too many tabs open
          </span>
          <span className="text-xs text-muted-foreground" style={{ fontFamily: "'JetBrains Mono', monospace" }}>
            © 2025 · made with love, not vc funding
          </span>
        </div>
      </footer>
    </div>
  );
}
