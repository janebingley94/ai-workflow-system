export default function HomePage() {
  return (
    <main className="space-y-6">
      <header className="space-y-2">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Phase 1</p>
        <h1 className="text-3xl font-semibold">AI Workflow System</h1>
        <p className="text-slate-300">
          Backend node system is implemented. Frontend editor will arrive in later phases.
        </p>
      </header>
      <section className="grid gap-4 md:grid-cols-3">
        {[
          { title: "New Workflow", path: "/workflow/new" },
          { title: "Edit Workflow", path: "/workflow/demo/edit" },
          { title: "Run Workflow", path: "/workflow/demo/run" },
        ].map((item) => (
          <a
            key={item.title}
            href={item.path}
            className="rounded-xl border border-slate-800 bg-slate-900 p-4 transition hover:border-slate-600"
          >
            <h2 className="text-lg font-medium">{item.title}</h2>
            <p className="text-sm text-slate-400">Placeholder page</p>
          </a>
        ))}
      </section>
    </main>
  );
}
