import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Leaf, Zap, Droplets, Trash2 } from 'lucide-react';

export default function Sustainability() {
  const [data, setData] = useState<any>(null);
  const [insight, setInsight] = useState("Analyzing metrics...");

  useEffect(() => {
    fetch('http://localhost:8000/api/sustainability/')
      .then(res => res.json())
      .then(setData);
    
    fetch('http://localhost:8000/api/sustainability/insight')
      .then(res => res.json())
      .then(d => setInsight(d.insight));
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Sustainability Dashboard</h2>
      
      <Card className="bg-green-500/10 border-green-500/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-500">
            <Leaf /> AI Sustainability Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg text-foreground/80">{insight}</p>
        </CardContent>
      </Card>

      {data && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Power Usage</CardTitle>
              <Zap className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.power_usage_kw} kW</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Water Usage</CardTitle>
              <Droplets className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.water_usage_l} L</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Waste Generated</CardTitle>
              <Trash2 className="h-4 w-4 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{data.waste_generation_kg} kg</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Surplus Food</CardTitle>
              <Leaf className="h-4 w-4 text-green-500" />
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
