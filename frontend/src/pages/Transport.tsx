import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bus, Train, Car } from 'lucide-react';
import { apiUrl } from '@/config/api';

/** Shape of transport status data from the API. */
interface TransportItem {
  route: string;
  status: string;
}

export default function Transport() {
  const [data, setData] = useState<TransportItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch(apiUrl('/api/transport/'))
      .then(res => res.json())
      .then((items: TransportItem[]) => {
        setData(items);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const getIcon = (route: string) => {
    if (route.includes("Metro")) return <Train className="text-blue-500" aria-hidden="true" />;
    if (route.includes("Bus")) return <Bus className="text-green-500" aria-hidden="true" />;
    return <Car className="text-orange-500" aria-hidden="true" />;
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Transportation Hub</h1>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3" role="list" aria-label="Transport routes" aria-busy={loading}>
        {data.map((item, i) => (
          <Card key={i} role="listitem">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-lg font-medium">{item.route}</CardTitle>
              {getIcon(item.route)}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mt-2">{item.status}</div>
              {item.status.includes("Full") || item.status.includes("Delay") ? (
                <p className="text-xs text-destructive mt-1" role="alert">Consider alternative routes</p>
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
