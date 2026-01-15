// src/components/ChatbotWidget.jsx
import React, { useState, useEffect, useRef } from "react";
import { Input, List, Card } from "antd";
import axios from "axios";
import showdown from 'showdown';
import '../chat.css'

const { TextArea } = Input;

// Create a Showdown converter instance
const converter = new showdown.Converter({
  tables: true,
  tasklists: true,
  strikethrough: true,
  emoji: true
});

// Component to render markdown as HTML
const MarkdownMessage = ({ text }) => {
  const html = converter.makeHtml(text);
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
};

// Use Vite env var VITE_API_BASE_URL; fallback to localhost
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const CHAT_ENDPOINT = `${API_BASE}/app/v1/chat/`;
const SESSIONS_ENDPOINT = `${API_BASE}/app/v1/chat/sessions`;

// LocalStorage key for session persistence
const SESSION_STORAGE_KEY = 'chatbot_session_id';

const ChatbotWidget = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const messageEndRef = useRef(null);

  // Initialize session on component mount
  useEffect(() => {
    const initializeSession = async () => {
      try {
        // Check if we have a stored session ID
        const storedSessionId = localStorage.getItem(SESSION_STORAGE_KEY);
        
        if (storedSessionId) {
          // Try to load existing session
          try {
            const sessionRes = await axios.get(
              `${SESSIONS_ENDPOINT}/${storedSessionId}`
            );
            const session = sessionRes.data;
            
            // Restore messages from session history
            if (session.messages && session.messages.length > 0) {
              const restoredMessages = session.messages.map(msg => ({
                from: msg.role === 'user' ? 'user' : 'bot',
                text: msg.content
              }));
              setMessages(restoredMessages);
            } else {
              // Session exists but no messages, show welcome
              setMessages([{ from: "bot", text: "Hi, how can I help you?" }]);
            }
            
            setSessionId(storedSessionId);
            setIsInitializing(false);
            return;
          } catch (err) {
            // Session not found or expired, create new one
            console.log('Stored session not found, creating new session');
            localStorage.removeItem(SESSION_STORAGE_KEY);
          }
        }
        
        // Create new session
        const sessionRes = await axios.post(SESSIONS_ENDPOINT);
        const newSession = sessionRes.data;
        setSessionId(newSession.session_id);
        localStorage.setItem(SESSION_STORAGE_KEY, newSession.session_id);
        
        setMessages([{ from: "bot", text: "Hi, how can I help you?" }]);
      } catch (err) {
        console.error('Failed to initialize session:', err);
        setMessages([{ 
          from: "bot", 
          text: "Error: Unable to initialize chat session. Please refresh the page." 
        }]);
      } finally {
        setIsInitializing(false);
      }
    };

    initializeSession();
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || isLoading || !sessionId) return;
    
    const userMsg = input.trim();
    const currentInput = input;

    // Optimistically add user message
    setMessages((prev) => [...prev, { from: "user", text: userMsg }]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post(CHAT_ENDPOINT, {
        query: currentInput,
        session_id: sessionId, // Include session_id in request
      });
      
      // Update session_id if backend generated a new one (shouldn't happen, but safe)
      if (res.data.session_id && res.data.session_id !== sessionId) {
        setSessionId(res.data.session_id);
        localStorage.setItem(SESSION_STORAGE_KEY, res.data.session_id);
      }
      
      // Add bot response
      setMessages((prev) => [...prev, { from: "bot", text: res.data.response }]);
    } catch (err) {
      console.error('Chat request failed:', err);
      const errText = err?.response?.data?.detail || err?.message || 'Error: No response';
      setMessages((prev) => [...prev, { from: "bot", text: `Error: ${errText}` }]);
      
      // If session error, try to create a new session
      if (err?.response?.status === 404 || err?.response?.status === 400) {
        try {
          const sessionRes = await axios.post(SESSIONS_ENDPOINT);
          const newSession = sessionRes.data;
          setSessionId(newSession.session_id);
          localStorage.setItem(SESSION_STORAGE_KEY, newSession.session_id);
        } catch (sessionErr) {
          console.error('Failed to recreate session:', sessionErr);
        }
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !isLoading) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Show loading state during initialization
  if (isInitializing) {
    return (
      <Card title="AI Chatbot" className="card-title">
        <div className="message-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div>Initializing chat...</div>
        </div>
      </Card>
    );
  }

  return (
    <Card title="AI Chatbot" className="card-title">
      <div className="message-container">
        <List
          dataSource={messages}
          renderItem={(item) => (
            <List.Item className={`text-message ${item.from === 'user' ? 'user' : 'bot'}`}>
              {item.from === 'user' ? (
                <div>{item.text}</div>
              ) : (
                <MarkdownMessage text={item.text} />
              )}
            </List.Item>
          )}
        />
        <div ref={messageEndRef} />
      </div>
      <TextArea
        className="text-area"
        rows={2}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={isLoading ? "Sending..." : "Type your message..."}
        disabled={isLoading}
      />
    </Card>
  );
};

export default ChatbotWidget;