import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { apiUrl } from '@/config/api';

/** Shape of crowd occupancy data for a single zone. */
interface CrowdDataItem {
  location: string;
  occupancy_percent: number;
}

export default function Crowd() {
  const [data, setData] = useState<CrowdDataItem[]>([]);
  const [insight, setInsight] = useState<string>("Analyzing crowd data...");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [crowdRes, insightRes] = await Promise.all([
          fetch(apiUrl('/api/crowd/')),
          fetch(apiUrl('/api/crowd/insight')),
        ]);
        const crowdData: CrowdDataItem[] = await crowdRes.json();
        const insightData = await insightRes.json();
        setData(crowdData);
        setInsight(insightData.insight);
      } catch {
        setInsight("Failed to load crowd data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Crowd Intelligence</h1>

      <Card className="bg-destructive/10 border-destructive/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-destructive">
            <AlertCircle aria-hidden="true" /> AI Crowd Alert &amp; Insight
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p
            className="text-lg text-destructive-foreground"
            aria-live="polite"
            aria-busy={loading}
          >
            {insight}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Real-Time Occupancy by Zone</CardTitle>
        </CardHeader>
        <CardContent className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              role="img"
              aria-label="Bar chart showing occupancy percentage by stadium zone"
            >
              <XAxis type="number" domain={[0, 100]} />
              <YAxis dataKey="location" type="category" width={120} />
              <Tooltip
                cursor={{ fill: 'transparent' }}
                contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))' }}
              />
              <Bar dataKey="occupancy_percent" radius={[0, 4, 4, 0]} name="Occupancy (%)">
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.occupancy_percent > 85 ? 'hsl(var(--destructive))' : 'hsl(var(--primary))'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
