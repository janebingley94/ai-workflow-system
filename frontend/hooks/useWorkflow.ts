"use client";

import { useCallback, useEffect, useState } from "react";

import { api } from "@/lib/api";
import type { FlowConfig, Workflow } from "@/lib/types";

export function useWorkflowList() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listWorkflows();
      setWorkflows(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load workflows");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { workflows, loading, error, refresh };
}

export function useWorkflowDetail(id?: string) {
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!id) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await api.getWorkflow(id);
      setWorkflow(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load workflow");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    void load();
  }, [load]);

  const save = useCallback(
    async (name: string, flow_config: FlowConfig) => {
      if (!id) return null;
      const updated = await api.updateWorkflow(id, name, flow_config);
      setWorkflow(updated);
      return updated;
    },
    [id]
  );

  return { workflow, loading, error, refresh: load, save };
}
