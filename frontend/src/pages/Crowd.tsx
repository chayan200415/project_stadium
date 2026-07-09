import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Crowd() {
  const [data, setData] = useState<any[]>([]);
  const [insight, setInsight] = useState("Analyzing crowd data...");

  useEffect(() => {
    fetch('https://project-stadium.onrender.com/api/crowd/')
      .then(res => res.json())
      .then(setData);
    
    fetch('https://project-stadium.onrender.com/api/crowd/insight')
      .then(res => res.json())
      .then(d => setInsight(d.insight));
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Crowd Intelligence</h2>
      
      <Card className="bg-destructive/10 border-destructive/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-destructive">
            <AlertCircle /> AI Crowd Alert & Insight
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg text-destructive-foreground">{insight}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Real-Time Occupancy by Zone</CardTitle>
        </CardHeader>
        <CardContent className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <XAxis type="number" domain={[0, 100]} />
              <YAxis dataKey="location" type="category" width={120} />
              <Tooltip cursor={{fill: 'transparent'}} contentStyle={{backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))'}}/>
              <Bar dataKey="occupancy_percent" radius={[0, 4, 4, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.occupancy_percent > 85 ? 'hsl(var(--destructive))' : 'hsl(var(--primary))'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
