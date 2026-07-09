import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MapPin, Navigation as NavIcon } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export default function Navigation() {
  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Indoor Navigation</h2>
      
      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Route Planner</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Starting Point</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input className="pl-9" placeholder="e.g. Gate 5" />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Destination</label>
              <div className="relative">
                <NavIcon className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input className="pl-9" placeholder="e.g. Section 112, Row B" />
              </div>
            </div>
            <Button className="w-full">Find Route</Button>
          </CardContent>
        </Card>
        
        <Card className="lg:col-span-2 min-h-[500px] flex items-center justify-center bg-secondary/20 relative overflow-hidden">
          {/* Placeholder for Leaflet map */}
          <div className="text-center p-8 backdrop-blur-md bg-background/50 rounded-xl border border-border shadow-xl">
            <MapPin className="h-12 w-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold mb-2">Interactive 3D Map</h3>
            <p className="text-muted-foreground text-sm max-w-sm">
              The stadium map will load here. Select a starting point and destination to see the optimal route.
            </p>
          </div>
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1577223625816-7546f13df25d?q=80&w=1200&auto=format&fit=crop')] opacity-10 bg-cover bg-center -z-10" />
        </Card>
      </div>
    </div>
  );
}
