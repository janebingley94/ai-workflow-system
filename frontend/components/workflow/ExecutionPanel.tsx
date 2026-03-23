"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import type { ExecutionEvent } from "@/lib/types";

export function ExecutionPanel({
  onRun,
  events,
  running,
  error,
}: {
  onRun: (input: string) => void;
  events: ExecutionEvent[];
  running: boolean;
  error?: string | null;
}) {
  const [input, setInput] = useState("Write a launch plan for a new AI workflow.");

  const latestOutput = useMemo(() => {
    const done = [...events].reverse().find((event) => event.type === "done");
    return done?.output;
  }, [events]);

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <Badge variant="accent">Execution</Badge>
          <h3 className="mt-2 text-lg font-semibold">Run Workflow</h3>
        </div>
        <Button onClick={() => onRun(input)} disabled={running}>
          {running ? "Running..." : "Run"}
        </Button>
      </div>
      <Textarea value={input} onChange={(event) => setInput(event.target.value)} />
      {error && <p className="text-sm text-rose-300">{error}</p>}

      <div className="grid gap-3 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Stream</p>
        <div className="max-h-48 space-y-2 overflow-auto text-xs text-slate-300">
          {events.length === 0 && <p className="text-slate-500">No events yet.</p>}
          {events.map((event, idx) => (
            <div key={`${event.type}-${idx}`} className="rounded-lg border border-slate-800 p-2">
              <div className="text-slate-400">{event.type}</div>
              <pre className="whitespace-pre-wrap text-slate-200">
                {JSON.stringify(event, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      </div>

      {latestOutput && (
        <div className="rounded-2xl border border-emerald-400/30 bg-emerald-400/10 p-4 text-sm text-emerald-100">
          <p className="text-xs uppercase tracking-[0.3em] text-emerald-200">Final Output</p>
          <pre className="mt-2 whitespace-pre-wrap">{JSON.stringify(latestOutput, null, 2)}</pre>
        </div>
      )}
    </section>
  );
}
