import { NodeProps } from "reactflow";

import { NodeShell } from "./NodeShell";

export function VectorStoreNode({ data }: NodeProps) {
  return (
    <NodeShell title={data.label || "Vector Store"} subtitle="Retrieval" accent="amber">
      <div>Index: {data.index || "default"}</div>
      <div className="text-slate-500">Top K: {data.top_k ?? 3}</div>
    </NodeShell>
  );
}
