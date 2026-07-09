import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bus, Train, Car } from 'lucide-react';

export default function Transport() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/transport/')
      .then(res => res.json())
      .then(setData);
  }, []);

  const getIcon = (route: string) => {
    if (route.includes("Metro")) return <Train className="text-blue-500" />;
    if (route.includes("Bus")) return <Bus className="text-green-500" />;
    return <Car className="text-orange-500" />;
  };

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Transportation Hub</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data.map((item, i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-lg font-medium">{item.route}</CardTitle>
              {getIcon(item.route)}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mt-2">{item.status}</div>
              {item.status.includes("Full") || item.status.includes("Delay") ? (
                <p className="text-xs text-destructive mt-1">Consider alternative routes</p>
              ) : (
                <p className="text-xs text-muted-foreground mt-1">Normal service</p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
