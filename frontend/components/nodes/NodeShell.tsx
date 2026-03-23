import type { ReactNode } from "react";
import { Handle, Position } from "reactflow";

import { cn } from "@/lib/utils";

export type NodeShellProps = {
  title: string;
  subtitle?: string;
  accent?: string;
  children?: ReactNode;
  hideTarget?: boolean;
  hideSource?: boolean;
};

export function NodeShell({
  title,
  subtitle,
  accent = "emerald",
  children,
  hideTarget,
  hideSource,
}: NodeShellProps) {
  return (
    <div
      className={cn(
        "min-w-[220px] rounded-2xl border border-slate-800 bg-slate-900/90 p-4 text-slate-100 shadow-[0_15px_40px_rgba(0,0,0,0.35)]",
        accent === "amber" && "border-amber-400/40",
        accent === "sky" && "border-sky-400/40",
        accent === "rose" && "border-rose-400/40"
      )}
    >
      {!hideTarget && (
        <Handle type="target" position={Position.Left} className="!bg-slate-200" />
      )}
      <div className="space-y-1">
        <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{subtitle}</p>
        <h3 className="text-base font-semibold">{title}</h3>
      </div>
      {children && <div className="mt-3 text-xs text-slate-300">{children}</div>}
      {!hideSource && (
        <Handle type="source" position={Position.Right} className="!bg-emerald-300" />
      )}
    </div>
  );
}
