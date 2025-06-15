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

const ChatbotWidget = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messageEndRef = useRef(null);

   useEffect(() => {
    setMessages([{ from: "bot", text: "Hi, how can I help you?" }]);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input.trim();

    setMessages((prev) => [...prev, { from: "user", text: userMsg }]);
    setInput("");

    try {
      const res = await axios.post("/api/v1/chat/", {
        query: userMsg,
      });
      setMessages((prev) => [...prev, { from: "bot", text: res.data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { from: "bot", text: "Error: No response" }]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

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
        placeholder="Type your message..."
      />
    </Card>
  );
};

export default ChatbotWidget;
