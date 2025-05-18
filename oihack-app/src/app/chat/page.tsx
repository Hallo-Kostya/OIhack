"use client";

import React, { useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

interface Message {
  message: string;
  type: 'user' | 'ai';
  leadId?: string | null;
}

export default function Chat() {
    const [status, setStatus] = useState<'Подключение...' | 'Подключено' | 'Отключено'>('Подключение...');
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState<string>('');
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const ws = useRef<WebSocket | null>(null);
  
    useEffect(() => {
      // Подключение к WebSocket
      ws.current = new WebSocket('ws://localhost:8000/api/ws/chat');
  
      ws.current.onopen = () => {
        setStatus('Подключено');
      };
  
      ws.current.onclose = () => {
        setStatus('Отключено');
      };
  
      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'response') {
            addMessage(data.message, 'ai', data.lead_id);
          } else if (data.type === 'error') {
            addMessage('Ошибка: ' + data.message, 'ai');
          }
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };
  
      return () => {
        if (ws.current) {
          ws.current.close();
        }
      };
    }, []);
  
    const addMessage = (message: string, type: 'user' | 'ai', leadId: string | null = null) => {
      setMessages((prevMessages) => [...prevMessages, { message, type, leadId }]);
    };
  
    const sendMessage = () => {
      const message = inputValue.trim();
      if (message && ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ message }));
        addMessage(message, 'user');
        setInputValue('');
      }
    };
  
    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div 
        className="flex flex-col h-screen bg-gray-100"
        style={{
            backgroundImage: "url('/common/background_main.png')",
            backgroundSize: "cover",  
            backgroundPosition: "center", 
            width: "100%",           
            height: "100vh",         
            position: "relative"     
        }}
    >
      {/* Шапка чата */}
      <div className="flex mt-11 pb-3 shadow-sm">
        <Link href="/">
            <Image src={'/common/components/arrow_left.svg'} alt={'На главную страницу'}
                width={28}
                height={28}
                className={'flex justify-center align-center mt-4 ml-4'}>
            </Image>
        </Link>
        <div className="max-w-4xl mx-auto">
            <Image src={'/common/logo.png'} alt={'Логотип Очень Интересно'}
                width={32} height={31}
                className={'mx-auto'}>
            </Image>
          <h1 className="text-[14px] font-[500] text-white flex justify-center mt-2">Интересный чат-бот</h1>
          <span
            className={`flex justify-center mt-2 font-medium ${status === 'Подключено' ? 'text-gray-500' : status === 'Отключено' ? 'text-red-500' : 'text-yellow-500'}`}
          >
            {status}
          </span>
        </div>
      </div>

      {/* Область сообщений */}
      <div className="flex-1 overflow-y-auto p-4 max-w-4xl w-full mx-auto">
        <div className="space-y-3">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 py-10 pl-10">
              Начните диалог с AI-ассистентом
            </div>
          )}
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs md:max-w-md lg:max-w-lg rounded-lg p-2 px-4 ${msg.type === 'user' ? 'bg-white/10 text-white border border-gray-200/20' : 'bg-black/10 border border-gray-200/20'}`}
              >
                <p className="break-words">{msg.message}</p>
                {msg.leadId && (
                  <span className="text-xs opacity-70 block mt-1">
                    ID лида: {msg.leadId}
                  </span>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Фиксированное поле ввода */}
      <div className="border-t border-gray-200/20 p-4 sticky bottom-0">
        <div className="max-w-4xl mx-auto flex gap-2 flex-grow p-3 border border-gray-200/20 rounded-lg">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Введите сообщение..."
            className="focus:outline-none"
          />
          <button
            onClick={sendMessage}
            className="px-3 ml-auto text-white rounded-lg transition-colors"
            // Убрал disabled для тестирования
          >
            <Image src={'/common/components/chat_arrow.png'} alt={'Отправить сообщение'} width={24} height={24}>
                
            </Image>
          </button>
        </div>
      </div>
    </div>
  );
}