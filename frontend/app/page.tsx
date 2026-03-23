"use client";

import Link from "next/link";

import { WorkflowCard } from "@/components/workflow/WorkflowCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useWorkflowList } from "@/hooks/useWorkflow";

export default function HomePage() {
  const { workflows, loading, error } = useWorkflowList();

  return (
    <main className="space-y-8">
      <header className="space-y-3">
        <Badge variant="accent">AI Workflow System</Badge>
        <h1 className="text-4xl font-semibold">Design, wire, and run AI workflows.</h1>
        <p className="max-w-2xl text-slate-300">
          Drag nodes, configure parameters, and orchestrate LLM workflows with live execution traces.
        </p>
        <Link href="/workflow/new">
          <Button size="lg">Create New Workflow</Button>
        </Link>
      </header>

      <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {loading && <p className="text-slate-400">Loading workflows...</p>}
        {error && <p className="text-rose-300">{error}</p>}
        {!loading && workflows.length === 0 && (
          <div className="rounded-3xl border border-dashed border-slate-800 p-10 text-slate-400">
            No workflows yet. Create your first one.
          </div>
        )}
        {workflows.map((workflow) => (
          <WorkflowCard key={workflow.id} workflow={workflow} />
        ))}
      </section>
    </main>
  );
}
