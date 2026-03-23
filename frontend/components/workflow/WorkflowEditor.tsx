"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { NodePalette } from "@/components/workflow/NodePalette";
import { NodeProperties } from "@/components/workflow/NodeProperties";
import { WorkflowCanvas, useWorkflowCanvas } from "@/components/workflow/WorkflowCanvas";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import type { FlowConfig, WorkflowNode } from "@/lib/types";
import { useWorkflowDetail } from "@/hooks/useWorkflow";

const templateNodes: WorkflowNode[] = [
  {
    id: "input_1",
    type: "input",
    position: { x: 120, y: 200 },
    data: { label: "Input", input_key: "input" },
  },
  {
    id: "llm_1",
    type: "llm",
    position: { x: 420, y: 200 },
    data: { label: "LLM", model: "gpt-4o", temperature: 0.7 },
  },
  {
    id: "output_1",
    type: "output",
    position: { x: 720, y: 200 },
    data: { label: "Output", output_key: "output" },
  },
];

const templateEdges = [
  { id: "e1", source: "input_1", target: "llm_1" },
  { id: "e2", source: "llm_1", target: "output_1" },
];

export function WorkflowEditor({ mode, workflowId }: { mode: "create" | "edit"; workflowId?: string }) {
  const router = useRouter();
  const { workflow, loading } = useWorkflowDetail(mode === "edit" ? workflowId : undefined);
  const [name, setName] = useState("Untitled Workflow");
  const [selectedNode, setSelectedNode] = useState<WorkflowNode | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const initialNodes = useMemo(() => (workflow?.flow_config.nodes ?? templateNodes), [workflow]);
  const initialEdges = useMemo(() => (workflow?.flow_config.edges ?? templateEdges), [workflow]);

  const { nodes, edges, setNodes, setEdges, onNodesChange, onEdgesChange, addNode } =
    useWorkflowCanvas(initialNodes, initialEdges);

  useEffect(() => {
    if (workflow) {
      setName(workflow.name);
      setNodes(workflow.flow_config.nodes);
      setEdges(workflow.flow_config.edges);
    }
  }, [workflow, setNodes, setEdges]);

  const save = async () => {
    const flow_config: FlowConfig = {
      id: workflow?.flow_config.id,
      name,
      nodes,
      edges,
    };

    if (mode === "create") {
      const created = await api.createWorkflow(name, flow_config);
      router.push(`/workflow/${created.id}/edit`);
      return;
    }

    if (!workflowId) return;
    await api.updateWorkflow(workflowId, name, flow_config);
    setMessage("Saved successfully");
    setTimeout(() => setMessage(null), 2000);
  };

  const updateNodeData = (updates: Partial<WorkflowNode["data"]>) => {
    if (!selectedNode) return;
    setNodes((prev) =>
      prev.map((node) =>
        node.id === selectedNode.id
          ? { ...node, data: { ...node.data, ...updates } }
          : node
      )
    );
    setSelectedNode((prev) => (prev ? { ...prev, data: { ...prev.data, ...updates } } : prev));
  };

  return (
    <section className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <Badge variant="accent">Workflow Editor</Badge>
          <h1 className="mt-2 text-3xl font-semibold">{mode === "create" ? "New" : "Edit"} Workflow</h1>
        </div>
        <div className="flex items-center gap-3">
          {message && <span className="text-xs text-emerald-300">{message}</span>}
          <Button variant="outline" onClick={() => router.push("/")}>Back</Button>
          <Button onClick={save}>{mode === "create" ? "Create" : "Save"}</Button>
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-[240px_minmax(0,1fr)_260px]">
        <NodePalette onAddNode={addNode} />

        <div className="space-y-4">
          <div className="flex flex-col gap-2">
            <label className="text-xs uppercase tracking-[0.3em] text-slate-500">Name</label>
            <Input value={name} onChange={(event) => setName(event.target.value)} />
          </div>
          <WorkflowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onSelectNode={setSelectedNode}
          />
        </div>

        {selectedNode ? (
          <NodeProperties node={selectedNode} onChange={updateNodeData} />
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-700 p-6 text-sm text-slate-400">
            Select a node to edit its properties.
          </div>
        )}
      </div>

      {loading && <p className="text-sm text-slate-500">Loading workflow...</p>}
    </section>
  );
}
