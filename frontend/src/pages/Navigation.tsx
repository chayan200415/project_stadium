import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MapPin, Navigation as NavIcon, Accessibility } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { apiUrl } from '@/config/api';

/** Shape of the navigation response from the API. */
interface NavigationResult {
  start: string;
  end: string;
  steps: string[];
  estimated_time_mins: number;
  accessible_route: string[];
}

export default function Navigation() {
  const [start, setStart] = useState<string>('');
  const [end, setEnd] = useState<string>('');
  const [result, setResult] = useState<NavigationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [showAccessible, setShowAccessible] = useState<boolean>(false);

  const findRoute = async () => {
    if (!start.trim() || !end.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(
        apiUrl(`/api/navigation/?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`)
      );
      const data: NavigationResult = await res.json();
      setResult(data);
    } catch {
      // Error handled gracefully
    } finally {
      setLoading(false);
    }
  };

  const currentSteps = showAccessible && result ? result.accessible_route : result?.steps ?? [];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Indoor Navigation</h1>

      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Route Planner</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="nav-start" className="text-sm font-medium text-muted-foreground">
                Starting Point
              </label>
              <div className="relative">
                <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" aria-hidden="true" />
                <Input
                  id="nav-start"
                  className="pl-9"
                  placeholder="e.g. Gate 5"
                  value={start}
                  onChange={(e) => setStart(e.target.value)}
                  aria-label="Starting point"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label htmlFor="nav-end" className="text-sm font-medium text-muted-foreground">
                Destination
              </label>
              <div className="relative">
                <NavIcon className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" aria-hidden="true" />
                <Input
                  id="nav-end"
                  className="pl-9"
                  placeholder="e.g. Section 112, Row B"
                  value={end}
                  onChange={(e) => setEnd(e.target.value)}
                  aria-label="Destination"
                />
              </div>
            </div>
            <Button className="w-full" onClick={findRoute} disabled={loading || !start.trim() || !end.trim()}>
              {loading ? "Finding Route..." : "Find Route"}
            </Button>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2 min-h-[500px] flex flex-col bg-secondary/20 relative overflow-hidden">
          {result ? (
            <div className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold">
                  {result.start} → {result.end}
                </h2>
                <span className="text-sm text-muted-foreground bg-secondary px-3 py-1 rounded-full">
                  ~{result.estimated_time_mins} min
                </span>
              </div>

              <div className="flex gap-2">
                <Button
                  variant={!showAccessible ? "default" : "outline"}
                  size="sm"
                  onClick={() => setShowAccessible(false)}
                  aria-pressed={!showAccessible}
                >
                  Standard Route
                </Button>
                <Button
                  variant={showAccessible ? "default" : "outline"}
                  size="sm"
                  onClick={() => setShowAccessible(true)}
                  aria-pressed={showAccessible}
                >
                  <Accessibility className="mr-1 h-4 w-4" aria-hidden="true" />
                  Accessible Route
                </Button>
              </div>

              <ol className="space-y-3" aria-label={showAccessible ? "Accessible route steps" : "Standard route steps"}>
                {currentSteps.map((step, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center text-sm font-bold">
                      {i + 1}
                    </span>
                    <span className="text-foreground pt-1">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          ) : (
            <>
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center p-8 backdrop-blur-md bg-background/50 rounded-xl border border-border shadow-xl">
                  <MapPin className="h-12 w-12 text-primary mx-auto mb-4" aria-hidden="true" />
                  <h2 className="text-xl font-bold mb-2">Interactive Stadium Map</h2>
                  <p className="text-muted-foreground text-sm max-w-sm">
                    Enter a starting point and destination to see the optimal route with step-by-step directions.
                  </p>
                </div>
              </div>
              <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1577223625816-7546f13df25d?q=80&w=1200&auto=format&fit=crop')] opacity-10 bg-cover bg-center -z-10" role="presentation" />
            </>
          )}
        </Card>
      </div>
    </div>
  );
}
