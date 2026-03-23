"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { ExecutionPanel } from "@/components/workflow/ExecutionPanel";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useExecution } from "@/hooks/useExecution";
import { useWorkflowDetail } from "@/hooks/useWorkflow";

export default function RunWorkflowPage() {
  const params = useParams();
  const id = Array.isArray(params?.id) ? params.id[0] : (params?.id as string | undefined);

  const { workflow, loading } = useWorkflowDetail(id);
  const { events, running, error, run } = useExecution(id);

  return (
    <section className="space-y-8">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <Badge variant="accent">Execution</Badge>
          <h1 className="mt-2 text-3xl font-semibold">Run Workflow</h1>
          <p className="text-sm text-slate-400">{workflow?.name || "Loading..."}</p>
        </div>
        <Link href={id ? `/workflow/${id}/edit` : "/"}>
          <Button variant="outline">Back to Editor</Button>
        </Link>
      </header>

      {loading && <p className="text-slate-400">Loading workflow...</p>}
      {workflow && (
        <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-6">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Workflow Summary</p>
            <div className="mt-4 space-y-2 text-sm text-slate-300">
              <p>Name: {workflow.name}</p>
              <p>Nodes: {workflow.flow_config.nodes.length}</p>
              <p>Edges: {workflow.flow_config.edges.length}</p>
            </div>
          </div>
          <ExecutionPanel onRun={run} events={events} running={running} error={error} />
        </div>
      )}
    </section>
  );
}
