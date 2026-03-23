import { NodeProps } from "reactflow";

import { NodeShell } from "./NodeShell";

export function OutputNode({ data }: NodeProps) {
  return (
    <NodeShell title={data.label || "Output"} subtitle="Result" accent="emerald" hideSource>
      <div>Key: {data.output_key || "output"}</div>
    </NodeShell>
  );
}
