(function () {
  const style = document.createElement("style");
  style.textContent = `
    #chatbot-container {
      position: fixed; bottom: 20px; right: 20px; width: 300px;
      font-family: sans-serif; background: white; border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.2); padding: 10px; z-index: 9999;
    }
    #chatbot-messages { max-height: 200px; overflow-y: auto; font-size: 14px; }
    #chatbot-input { width: 100%; padding: 8px; margin-top: 8px; border-radius: 5px; border: 1px solid #ccc; }
  `;
  document.head.appendChild(style);

  const container = document.createElement("div");
  container.id = "chatbot-container";
  container.innerHTML = `
    <div id="chatbot-messages"></div>
    <input id="chatbot-input" placeholder="Ask a question..." />
  `;
  document.body.appendChild(container);

  const input = document.getElementById("chatbot-input");
  const messages = document.getElementById("chatbot-messages");

  input.addEventListener("keypress", async (e) => {
    if (e.key === "Enter" && input.value.trim()) {
      const userMsg = input.value.trim();
      messages.innerHTML += `<div><b>You:</b> ${userMsg}</div>`;
      input.value = "";

      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg })
      });
      const data = await res.json();
      console.log("API Response:", data);
      if (data.response) {
        messages.innerHTML += `<div><b>Bot:</b> ${data.response}</div>`;
      } else {
        messages.innerHTML += `<div><b>Bot:</b> Sorry, no response received.</div>`;
      }
      messages.scrollTop = messages.scrollHeight;
    }
  });
})();
