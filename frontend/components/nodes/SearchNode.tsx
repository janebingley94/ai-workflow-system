import { NodeProps } from "reactflow";

import { NodeShell } from "./NodeShell";

export function SearchNode({ data }: NodeProps) {
  return (
    <NodeShell title={data.label || "Search"} subtitle="Web Search" accent="sky">
      <div>Provider: {data.provider || "tavily"}</div>
      <div className="text-slate-500">Top K: {data.num_results ?? 5}</div>
    </NodeShell>
  );
}
