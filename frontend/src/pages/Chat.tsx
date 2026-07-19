import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Send, Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';
import { apiUrl } from '@/config/api';

/** Represents a single chat message. */
interface ChatMessage {
  role: 'user' | 'bot';
  content: string;
}

/** Supported languages for AI response translation. */
const SUPPORTED_LANGUAGES = [
  "English", "Spanish", "French", "Arabic", "Portuguese",
  "German", "Japanese", "Hindi", "Chinese", "Korean",
];

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'bot', content: 'Hello! I am your StadiumGPT assistant for the FIFA World Cup 2026. How can I help you today?' }
  ]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [language, setLanguage] = useState<string>('English');

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage: ChatMessage = { role: 'user', content: input };
    const newMsgs = [...messages, userMessage];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(apiUrl('/api/chat/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, language }),
      });
      const data = await res.json();
      const botMessage: ChatMessage = { role: 'bot', content: data.response };
      setMessages([...newMsgs, botMessage]);
    } catch {
      const errorMessage: ChatMessage = { role: 'bot', content: 'Sorry, I encountered an error. Please try again.' };
      setMessages([...newMsgs, errorMessage]);
    }
    setLoading(false);
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-3xl font-bold tracking-tight">AI Fan Assistant</h1>
        <div className="flex items-center gap-2">
          <label htmlFor="language-select" className="text-sm text-muted-foreground">
            Response Language:
          </label>
          <select
            id="language-select"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-secondary text-foreground border border-border rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            aria-label="Select response language"
          >
            {SUPPORTED_LANGUAGES.map((lang) => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>
        </div>
      </div>
      <Card className="flex-1 flex flex-col overflow-hidden">
        <div
          className="flex-1 overflow-y-auto p-4 space-y-4"
          role="log"
          aria-label="Chat messages"
          aria-live="polite"
        >
          {messages.map((msg, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={i}
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'bot' && (
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary" aria-hidden="true">
                  <Bot size={18} />
                </div>
              )}
              <div
                className={`px-4 py-2 rounded-2xl max-w-[80%] ${
                  msg.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-secondary text-secondary-foreground'
                }`}
                role={msg.role === 'bot' ? 'status' : undefined}
              >
                {msg.content}
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white" aria-hidden="true">
                  <User size={18} />
                </div>
              )}
            </motion.div>
          ))}
          {loading && (
            <div className="text-muted-foreground text-sm ml-12 animate-pulse" role="status" aria-live="assertive">
              StadiumGPT is thinking...
            </div>
          )}
        </div>
        <div className="p-4 bg-card border-t border-border flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            aria-label="Message input"
            disabled={loading}
            className="flex-1 bg-secondary/50 border-none"
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            aria-label="Send message"
            className="h-10 w-10 bg-primary text-primary-foreground rounded-lg flex items-center justify-center hover:bg-primary/90 transition-colors disabled:opacity-50"
          >
            <Send size={18} />
          </button>
        </div>
      </Card>
    </div>
  );
}
