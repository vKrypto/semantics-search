// src/widget.jsx
import ReactDOM from "react-dom/client";
import ChatbotWidget from "./components/ChatbotWidget";
import "antd/dist/reset.css"; // optional: only needed once
import chatbotStyles from './chat.css?inline'; // 👈 inject your styles

function mountChatbot(containerId = "wrapper") {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Container with id "${containerId}" not found.`);
    return;
  }

  // 👇 Inject style tag manually
  const style = document.createElement("style");
  style.textContent = chatbotStyles;
  document.head.appendChild(style);

  const root = ReactDOM.createRoot(container);
  root.render(<ChatbotWidget />);
}

window.ChatbotWidget = { mountChatbot };
