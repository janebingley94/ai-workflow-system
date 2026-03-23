import { NodeProps } from "reactflow";

import { NodeShell } from "./NodeShell";

export function InputNode({ data }: NodeProps) {
  return (
    <NodeShell title={data.label || "Input"} subtitle="Entry" accent="emerald" hideTarget>
      <div>Key: {data.input_key || "input"}</div>
    </NodeShell>
  );
}
