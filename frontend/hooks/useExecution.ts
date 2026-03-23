"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { api } from "@/lib/api";
import type { ExecutionEvent } from "@/lib/types";

export function useExecution(workflowId?: string) {
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    return () => {
      eventSourceRef.current?.close();
    };
  }, []);

  const reset = useCallback(() => {
    setEvents([]);
    setError(null);
  }, []);

  const run = useCallback(
    async (input: any) => {
      if (!workflowId) return;
      setRunning(true);
      setError(null);
      setEvents([]);
      try {
        const { execution_id } = await api.executeWorkflow(workflowId, input);
        const url = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/execution/${execution_id}/stream`;
        const source = new EventSource(url);
        eventSourceRef.current = source;

        source.onmessage = (event) => {
          try {
            const payload = JSON.parse(event.data) as ExecutionEvent;
            setEvents((prev) => [...prev, payload]);
            if (payload.type === "done" || payload.type === "error") {
              setRunning(false);
              source.close();
            }
          } catch (err) {
            setEvents((prev) => [...prev, { type: "raw", content: event.data }]);
          }
        };

        source.onerror = () => {
          setError("Execution stream disconnected");
          setRunning(false);
          source.close();
        };
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to execute workflow");
        setRunning(false);
      }
    },
    [workflowId]
  );

  return { events, running, error, run, reset };
}
