import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { AlertTriangle, Plus } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Operations() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  
  const [form, setForm] = useState({ type: '', location: '', description: '' });

  useEffect(() => {
    fetch('https://project-stadium.onrender.com/api/incident/')
      .then(res => res.json())
      .then(setIncidents);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('https://project-stadium.onrender.com/api/incident/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(form)
    });
    const newIncident = await res.json();
    setIncidents([newIncident, ...incidents]);
    setShowForm(false);
    setForm({ type: '', location: '', description: '' });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">Operations Center</h2>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="mr-2" size={16}/> Report Incident
        </Button>
      </div>

      {showForm && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle>New Incident Report</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm">Incident Type (e.g., Medical, Security)</label>
                  <Input required value={form.type} onChange={e => setForm({...form, type: e.target.value})} />
                </div>
                <div>
                  <label className="text-sm">Location</label>
                  <Input required value={form.location} onChange={e => setForm({...form, location: e.target.value})} />
                </div>
              </div>
              <div>
                <label className="text-sm">Description</label>
                <Input required value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
              </div>
              <Button type="submit">Generate AI Response Plan</Button>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4">
        {incidents.map((inc) => (
          <motion.div initial={{opacity: 0}} animate={{opacity: 1}} key={inc.id}>
            <Card className="border-l-4 border-l-destructive">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex justify-between items-center">
                  <span className="flex items-center gap-2"><AlertTriangle size={18} className="text-destructive"/> {inc.type} at {inc.location}</span>
                  <span className="text-xs px-2 py-1 bg-secondary rounded-full text-muted-foreground">{new Date(inc.reported_at).toLocaleTimeString()}</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">{inc.description}</p>
                {inc.ai_plan && (
                  <div className="bg-primary/5 p-4 rounded-md border border-primary/20">
                    <h4 className="font-semibold text-primary mb-2 flex items-center gap-2">🤖 AI Response Plan</h4>
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
