"use client";

import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import type { WorkflowNode } from "@/lib/types";

const configMap: Record<string, { key: string; label: string; type?: "text" | "number" | "textarea" }[]> = {
  input: [
    { key: "label", label: "Label" },
    { key: "input_key", label: "Input Key" },
  ],
  output: [
    { key: "label", label: "Label" },
    { key: "output_key", label: "Output Key" },
  ],
  search: [
    { key: "label", label: "Label" },
    { key: "provider", label: "Provider" },
    { key: "num_results", label: "Results", type: "number" },
  ],
  llm: [
    { key: "label", label: "Label" },
    { key: "model", label: "Model" },
    { key: "temperature", label: "Temperature", type: "number" },
    { key: "system_prompt", label: "System Prompt", type: "textarea" },
  ],
  vector_store: [
    { key: "label", label: "Label" },
    { key: "index", label: "Index" },
    { key: "top_k", label: "Top K", type: "number" },
  ],
  condition: [
    { key: "label", label: "Label" },
    { key: "condition", label: "Condition" },
    { key: "input_key", label: "Input Key" },
  ],
};

export function NodeProperties({
  node,
  onChange,
}: {
  node: WorkflowNode;
  onChange: (updates: Partial<WorkflowNode["data"]>) => void;
}) {
  const fields = configMap[node.type] || [{ key: "label", label: "Label" }];

  return (
    <aside className="w-full max-w-[260px] space-y-4">
      <div>
        <Badge variant="accent">Properties</Badge>
        <h3 className="mt-2 text-lg font-semibold">{node.data.label || node.type}</h3>
        <p className="text-xs text-slate-400">Edit node parameters</p>
      </div>
      <div className="space-y-3">
        {fields.map((field) => {
          const value = node.data[field.key] ?? "";
          if (field.type === "textarea") {
            return (
              <label key={field.key} className="block text-xs text-slate-400">
                {field.label}
                <Textarea
                  value={value}
                  onChange={(event) => onChange({ [field.key]: event.target.value })}
                />
              </label>
            );
          }
          return (
            <label key={field.key} className="block text-xs text-slate-400">
              {field.label}
              <Input
                type={field.type === "number" ? "number" : "text"}
                value={value}
                onChange={(event) =>
                  onChange({
                    [field.key]: field.type === "number" ? Number(event.target.value) : event.target.value,
                  })
                }
              />
            </label>
          );
        })}
      </div>
    </aside>
  );
}
