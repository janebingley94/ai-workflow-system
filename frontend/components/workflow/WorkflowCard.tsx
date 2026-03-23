"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { Workflow } from "@/lib/types";

export function WorkflowCard({ workflow }: { workflow: Workflow }) {
  return (
    <Card className="flex flex-col justify-between">
      <CardHeader>
        <CardTitle>{workflow.name}</CardTitle>
        <CardDescription>{workflow.flow_config.nodes.length} nodes</CardDescription>
      </CardHeader>
      <CardContent className="flex items-center justify-between">
        <Link href={`/workflow/${workflow.id}/edit`}>
          <Button size="sm" variant="outline">
            Edit
          </Button>
        </Link>
        <Link href={`/workflow/${workflow.id}/run`}>
          <Button size="sm">
            Run
            <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
