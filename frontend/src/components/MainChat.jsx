// src/components/ChatWidget.jsx
import { useState } from "react"; // ✅ Add this
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput
} from "@chatscope/chat-ui-kit-react";

export default function ChatWidget({ onSend }) {
  const [msgs, setMsgs] = useState([]); // useState is now defined correctly

  const handleSend = (text) => {
    const userMsg = { text, sender: "user", time: new Date().toLocaleTimeString() };
    setMsgs((prev) => [...prev, userMsg]);

    onSend(text, (replyText) =>
      setMsgs((prev) => [
        ...prev,
        { text: replyText, sender: "agent", time: new Date().toLocaleTimeString() }
      ])
    );
  };

  return (
    <div style={{ height: 300 }}>
      <MainContainer>
        <ChatContainer>
          <MessageList>
            {msgs.map((m, i) => (
              <Message key={i} model={{ message: m.text, sentTime: m.time, sender: m.sender }} />
            ))}
          </MessageList>
          <MessageInput placeholder="Ask about contract…" onSend={handleSend} />
        </ChatContainer>
      </MainContainer>
    </div>
  );
}
