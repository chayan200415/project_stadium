import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Leaf, Zap, Droplets, Trash2 } from 'lucide-react';
import { apiUrl } from '@/config/api';

/** Shape of sustainability metrics from the API. */
interface SustainabilityMetrics {
  power_usage_kw: number;
  water_usage_l: number;
  waste_generation_kg: number;
  surplus_food_portions: number;
}

export default function Sustainability() {
  const [data, setData] = useState<SustainabilityMetrics | null>(null);
  const [insight, setInsight] = useState<string>("Analyzing metrics...");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsRes, insightRes] = await Promise.all([
          fetch(apiUrl('/api/sustainability/')),
          fetch(apiUrl('/api/sustainability/insight')),
        ]);
        const metricsData: SustainabilityMetrics = await metricsRes.json();
        const insightData = await insightRes.json();
        setData(metricsData);
        setInsight(insightData.insight);
      } catch {
        setInsight("Failed to load sustainability data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Sustainability Dashboard</h1>

      <Card className="bg-green-500/10 border-green-500/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-500">
            <Leaf aria-hidden="true" /> AI Sustainability Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p
            className="text-lg text-foreground/80"
            aria-live="polite"
            aria-busy={loading}
          >
            {insight}
          </p>
        </CardContent>
      </Card>

      {data && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4" role="list" aria-label="Sustainability metrics">
          <Card role="listitem">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Power Usage</CardTitle>
              <Zap className="h-4 w-4 text-yellow-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.power_usage_kw} kW</div>
              <p className="text-xs text-muted-foreground mt-1">Current consumption</p>
            </CardContent>
          </Card>

          <Card role="listitem">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Water Usage</CardTitle>
              <Droplets className="h-4 w-4 text-blue-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.water_usage_l} L</div>
              <p className="text-xs text-muted-foreground mt-1">Current consumption</p>
            </CardContent>
          </Card>

          <Card role="listitem">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Waste Generated</CardTitle>
              <Trash2 className="h-4 w-4 text-orange-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.waste_generation_kg} kg</div>
              <p className="text-xs text-muted-foreground mt-1">Today's total</p>
            </CardContent>
          </Card>

          <Card role="listitem">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Surplus Food</CardTitle>
              <Leaf className="h-4 w-4 text-green-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.surplus_food_portions} portions</div>
              <p className="text-xs text-muted-foreground mt-1">Ready for redistribution</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
