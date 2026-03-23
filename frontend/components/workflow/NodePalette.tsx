"use client";

import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

const nodeTypes = [
  { type: "input", label: "Input" },
  { type: "search", label: "Search" },
  { type: "llm", label: "LLM" },
  { type: "vector_store", label: "Vector Store" },
  { type: "condition", label: "Condition" },
  { type: "output", label: "Output" },
];

export function NodePalette({ onAddNode }: { onAddNode: (type: string) => void }) {
  return (
    <aside className="w-full max-w-[220px] space-y-4">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Nodes</p>
        <h3 className="mt-2 text-lg font-semibold">Node Palette</h3>
      </div>
      <div className="space-y-2">
        {nodeTypes.map((node) => (
          <Button
            key={node.type}
            variant="outline"
            className="w-full justify-between"
            onClick={() => onAddNode(node.type)}
          >
            {node.label}
            <Plus className="h-4 w-4" />
          </Button>
        ))}
      </div>
    </aside>
  );
}
