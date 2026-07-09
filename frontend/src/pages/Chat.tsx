import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Send, Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Chat() {
  const [messages, setMessages] = useState<{role: 'user'|'bot', content: string}[]>([
    {role: 'bot', content: 'Hello! I am your StadiumGPT assistant. How can I help you today?'}
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMsgs = [...messages, {role: 'user' as const, content: input}];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/chat/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: input, language: 'English' })
      });
      const data = await res.json();
      setMessages([...newMsgs, {role: 'bot' as const, content: data.response}]);
    } catch (e) {
      setMessages([...newMsgs, {role: 'bot' as const, content: 'Sorry, I encountered an error.'}]);
    }
    setLoading(false);
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <h2 className="text-3xl font-bold tracking-tight mb-4">AI Fan Assistant</h2>
      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <motion.div 
              initial={{opacity: 0, y: 10}} animate={{opacity: 1, y: 0}}
              key={i} 
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'bot' && <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary"><Bot size={18}/></div>}
              <div className={`px-4 py-2 rounded-2xl max-w-[80%] ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
                {msg.content}
              </div>
              {msg.role === 'user' && <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white"><User size={18}/></div>}
            </motion.div>
          ))}
          {loading && <div className="text-muted-foreground text-sm ml-12 animate-pulse">StadiumGPT is thinking...</div>}
        </CardContent>
        <div className="p-4 bg-card border-t border-border flex gap-2">
          <Input 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about gates, food, restrooms..."
            className="flex-1 bg-secondary/50 border-none"
          />
          <Button onClick={sendMessage} disabled={loading}><Send size={18} className="mr-2"/> Send</Button>
        </div>
      </Card>
    </div>
  );
}
