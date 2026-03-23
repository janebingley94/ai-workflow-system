"use client";

import { useCallback } from "react";
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  type Connection,
  type Edge,
  useEdgesState,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";

import { ConditionNode } from "@/components/nodes/ConditionNode";
import { InputNode } from "@/components/nodes/InputNode";
import { LLMNode } from "@/components/nodes/LLMNode";
import { OutputNode } from "@/components/nodes/OutputNode";
import { SearchNode } from "@/components/nodes/SearchNode";
import { VectorStoreNode } from "@/components/nodes/VectorStoreNode";
import type { WorkflowEdge, WorkflowNode } from "@/lib/types";

const nodeTypes = {
  llm: LLMNode,
  search: SearchNode,
  vector_store: VectorStoreNode,
  condition: ConditionNode,
  input: InputNode,
  output: OutputNode,
};

const defaults: Record<string, Record<string, any>> = {
  input: { label: "Input", input_key: "input" },
  output: { label: "Output", output_key: "output" },
  search: { label: "Search", provider: "tavily", num_results: 5 },
  llm: { label: "LLM", model: "gpt-4o", temperature: 0.7 },
  vector_store: { label: "Vector Store", index: "default", top_k: 3 },
  condition: { label: "Condition", condition: "contains:keyword", input_key: "input" },
};

function createNode(type: string, index: number): WorkflowNode {
  const base = defaults[type] || { label: type };
  return {
    id: `${type}_${Date.now()}_${index}`,
    type,
    position: { x: 200 + index * 40, y: 120 + index * 40 },
    data: { ...base },
  };
}

export function WorkflowCanvas({
  nodes,
  edges,
  onNodesChange,
  onEdgesChange,
  onSelectNode,
}: {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  onNodesChange: ReturnType<typeof useNodesState>[2];
  onEdgesChange: ReturnType<typeof useEdgesState>[2];
  onSelectNode: (node: WorkflowNode | null) => void;
}) {
  const onConnect = useCallback(
    (params: Edge | Connection) => onEdgesChange((eds) => addEdge(params, eds)),
    [onEdgesChange]
  );

  return (
    <div className="relative h-[720px] rounded-3xl border border-slate-800 bg-slate-950/70">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={(_, node) => onSelectNode(node as WorkflowNode)}
        onPaneClick={() => onSelectNode(null)}
        nodeTypes={nodeTypes}
        fitView
      >
        <Controls />
        <MiniMap />
        <Background gap={18} size={1} />
      </ReactFlow>
      <div className="pointer-events-none absolute right-8 top-8 rounded-full border border-slate-700 bg-slate-900/80 px-4 py-2 text-xs text-slate-400">
        Add nodes from palette
      </div>
    </div>
  );
}

export function useWorkflowCanvas(initialNodes: WorkflowNode[], initialEdges: WorkflowEdge[]) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const addNode = useCallback(
    (type: string) => {
      setNodes((prev) => [...prev, createNode(type, prev.length + 1)]);
    },
    [setNodes]
  );

  return {
    nodes,
    edges,
    setNodes,
    setEdges,
    onNodesChange,
    onEdgesChange,
    addNode,
  };
}
