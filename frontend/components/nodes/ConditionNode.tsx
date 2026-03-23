import { NodeProps } from "reactflow";

import { NodeShell } from "./NodeShell";

export function ConditionNode({ data }: NodeProps) {
  return (
    <NodeShell title={data.label || "Condition"} subtitle="Branch" accent="rose">
      <div>Rule: {data.condition || "contains:keyword"}</div>
      <div className="text-slate-500">Input: {data.input_key || "input"}</div>
    </NodeShell>
  );
}
