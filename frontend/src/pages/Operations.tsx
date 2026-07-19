import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { AlertTriangle, Plus } from 'lucide-react';
import { motion } from 'framer-motion';
import { apiUrl } from '@/config/api';

/** Shape of an incident returned from the API. */
interface IncidentItem {
  id: number;
  type: string;
  location: string;
  status: string;
  reported_at: string;
  description: string;
  ai_plan: string | null;
}

/** Shape of the incident creation form. */
interface IncidentForm {
  type: string;
  location: string;
  description: string;
}

export default function Operations() {
  const [incidents, setIncidents] = useState<IncidentItem[]>([]);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState<boolean>(false);

  const [form, setForm] = useState<IncidentForm>({ type: '', location: '', description: '' });

  useEffect(() => {
    fetch(apiUrl('/api/incident/'))
      .then(res => res.json())
      .then((data: IncidentItem[]) => setIncidents(data))
      .catch(() => setIncidents([]));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch(apiUrl('/api/incident/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const newIncident: IncidentItem = await res.json();
      setIncidents([newIncident, ...incidents]);
      setShowForm(false);
      setForm({ type: '', location: '', description: '' });
    } catch {
      // Error is handled gracefully
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Operations Center</h1>
        <Button onClick={() => setShowForm(!showForm)} aria-expanded={showForm}>
          <Plus className="mr-2" size={16} aria-hidden="true" /> Report Incident
        </Button>
      </div>

      {showForm && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle>New Incident Report</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4" aria-label="Incident report form">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="incident-type" className="text-sm font-medium">
                    Incident Type <span className="text-destructive">*</span>
                  </label>
                  <Input
                    id="incident-type"
                    required
                    aria-required="true"
                    placeholder="e.g., Medical, Security"
                    value={form.type}
                    onChange={e => setForm({ ...form, type: e.target.value })}
                  />
                </div>
                <div>
                  <label htmlFor="incident-location" className="text-sm font-medium">
                    Location <span className="text-destructive">*</span>
                  </label>
                  <Input
                    id="incident-location"
                    required
                    aria-required="true"
                    placeholder="e.g., Gate A, Section 112"
                    value={form.location}
                    onChange={e => setForm({ ...form, location: e.target.value })}
                  />
                </div>
              </div>
              <div>
                <label htmlFor="incident-description" className="text-sm font-medium">
                  Description <span className="text-destructive">*</span>
                </label>
                <Input
                  id="incident-description"
                  required
                  aria-required="true"
                  placeholder="Describe the incident in detail..."
                  value={form.description}
                  onChange={e => setForm({ ...form, description: e.target.value })}
                />
              </div>
              <Button type="submit" disabled={submitting} aria-busy={submitting}>
                {submitting ? "Generating..." : "Generate AI Response Plan"}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4" role="list" aria-label="Incident list">
        {incidents.map((inc) => (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} key={inc.id} role="listitem">
            <Card className="border-l-4 border-l-destructive">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex justify-between items-center">
                  <span className="flex items-center gap-2">
                    <AlertTriangle size={18} className="text-destructive" aria-hidden="true" />
                    {inc.type} at {inc.location}
                  </span>
                  <span className="text-xs px-2 py-1 bg-secondary rounded-full text-muted-foreground">
                    <time dateTime={inc.reported_at}>{new Date(inc.reported_at).toLocaleTimeString()}</time>
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">{inc.description}</p>
                {inc.ai_plan && (
                  <div className="bg-primary/5 p-4 rounded-md border border-primary/20">
                    <h3 className="font-semibold text-primary mb-2 flex items-center gap-2">🤖 AI Response Plan</h3>
                    <pre className="text-sm whitespace-pre-wrap font-sans text-muted-foreground">{inc.ai_plan}</pre>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
