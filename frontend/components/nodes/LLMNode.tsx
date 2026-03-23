import { NodeProps } from "reactflow";

import { NodeShell } from "./NodeShell";

export function LLMNode({ data }: NodeProps) {
  return (
    <NodeShell title={data.label || "LLM"} subtitle="AI Model" accent="emerald">
      <div>Model: {data.model || "gpt-4o"}</div>
      <div className="text-slate-500">Temp: {data.temperature ?? 0.7}</div>
    </NodeShell>
  );
}
