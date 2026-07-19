import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Users, Bus, AlertTriangle, Leaf, Train } from 'lucide-react';
import { apiUrl } from '@/config/api';

/** Shape of the transport status data from the API. */
interface TransportItem {
  route: string;
  status: string;
}

/** Shape of the sustainability metrics from the API. */
interface SustainabilityMetrics {
  power_usage_kw: number;
  water_usage_l: number;
  waste_generation_kg: number;
  surplus_food_portions: number;
}

export default function Dashboard() {
  const [summary, setSummary] = useState<string>("Loading AI summary...");
  const [transport, setTransport] = useState<TransportItem[]>([]);
  const [sustainability, setSustainability] = useState<SustainabilityMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, transportRes, sustainRes] = await Promise.all([
          fetch(apiUrl('/api/dashboard/summary')),
          fetch(apiUrl('/api/transport/')),
          fetch(apiUrl('/api/sustainability/')),
        ]);

        const summaryData = await summaryRes.json();
        const transportData = await transportRes.json();
        const sustainData = await sustainRes.json();

        setSummary(summaryData.summary);
        setTransport(transportData);
        setSustainability(sustainData);
      } catch {
        setSummary("Failed to load summary.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const activeTransportIssues = transport.filter(
    (t) => t.status.includes("Full") || t.status.includes("Delay") || t.status.includes("Heavy")
  ).length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Stadium Overview</h1>
        <span className="text-sm text-muted-foreground px-3 py-1 bg-primary/10 rounded-full">
          ⚽ FIFA World Cup 2026
        </span>
      </div>

      <Card className="bg-gradient-to-br from-primary/10 via-primary/5 to-background border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="text-primary" aria-hidden="true" />
            AI Match Day Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p
            className="text-lg leading-relaxed text-muted-foreground"
            aria-live="polite"
            aria-busy={loading}
          >
            {summary}
          </p>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Attendance</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">64,231</div>
            <p className="text-xs text-muted-foreground">+2% from last hour</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Incidents</CardTitle>
            <AlertTriangle className="h-4 w-4 text-destructive" aria-hidden="true" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">1 medical, 2 security</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Transport Alerts</CardTitle>
            <Bus className="h-4 w-4 text-orange-500" aria-hidden="true" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeTransportIssues}</div>
            <p className="text-xs text-muted-foreground">
              {activeTransportIssues > 0 ? "Routes with delays or full" : "All routes running smoothly"}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Sustainability Score</CardTitle>
            <Leaf className="h-4 w-4 text-green-500" aria-hidden="true" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {sustainability ? `${sustainability.power_usage_kw} kW` : "—"}
            </div>
            <p className="text-xs text-muted-foreground">Current power consumption</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
