import React, { useState, useRef, useEffect } from 'react';
import { Send, Gem, Sparkles } from './Icons';
import { Message } from '../types';
import { sendMessage } from '../services/geminiService';

export default function AiAssistantView() {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'model', text: 'The Arcane Oracle is listening. Speak your query, champion.', timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      text: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsLoading(true);

    try {
      const responseText = await sendMessage(userMsg.text);
      
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'model',
        text: responseText,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMsg]);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] relative rounded border border-azeroth-gold/30 bg-black/60 shadow-titan-glow bg-noise">
      <div className="absolute inset-0 opacity-10 pointer-events-none flex items-center justify-center">
        <Gem className="w-64 h-64 text-azeroth-gold animate-spin-slow" style={{ animationDuration: '30s' }} />
      </div>

      <div className="p-3 border-b border-azeroth-gold/20 bg-black/40 flex justify-between items-center z-10 relative">
        <span className="text-xs font-warcraft text-azeroth-gold tracking-widest uppercase flex items-center">
          <Sparkles className="w-4 h-4 mr-2" />
          Arcane Communication
        </span>
        <span className="text-[10px] text-slate-500 font-mono">Channel: Secure</span>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar relative z-10">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
          >
            <div
              className={`max-w-[85%] md:max-w-[70%] p-3 rounded text-sm font-sans leading-relaxed relative ${
                msg.role === 'user'
                  ? 'bg-rarity-epic/20 text-white border border-rarity-epic/40'
                  : 'bg-black/60 text-rarity-artifact border border-azeroth-gold/30'
              }`}
            >
              <div className="text-[10px] opacity-70 mb-1 font-warcraft uppercase tracking-wider flex items-center justify-between">
                <span className={msg.role === 'user' ? 'text-rarity-epic' : 'text-azeroth-gold'}>
                  {msg.role === 'user' ? 'You' : 'Oracle'} says:
                </span>
                <span className="text-slate-500 font-mono text-[9px]">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <p className="text-shadow">{msg.text}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start animate-pulse">
            <div className="bg-black/60 p-3 rounded border border-azeroth-gold/30 flex items-center space-x-2">
              <span className="text-xs text-azeroth-gold font-warcraft uppercase tracking-widest">Casting Divination</span>
              <div className="flex space-x-1">
                <div className="w-1 h-1 bg-azeroth-gold rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                <div className="w-1 h-1 bg-azeroth-gold rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-1 h-1 bg-azeroth-gold rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 z-20 relative bg-black/80 border-t border-azeroth-gold/20">
        <div className="relative flex items-center bg-black/60 border border-white/10 rounded focus-within:border-azeroth-gold/50 transition-colors">
          <div className="pl-3 pr-2">
            <span className="text-azeroth-gold font-warcraft text-sm opacity-80 text-shadow-glow">{'>'}</span>
          </div>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Incant your query..."
            className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-slate-600 px-2 py-3 font-sans tracking-wide text-sm"
          />
          <div className="pr-1">
            <button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className={`p-2 rounded-sm transition-all duration-300 font-warcraft uppercase text-[10px] tracking-widest border ${
                inputValue.trim() 
                  ? 'bg-azeroth-gold/10 text-azeroth-gold border-azeroth-gold/50 hover:bg-azeroth-gold hover:text-black hover:shadow-glow-gold' 
                  : 'text-slate-600 border-transparent cursor-not-allowed'
              }`}
            >
              Cast
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
