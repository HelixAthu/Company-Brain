import React, { useEffect, useRef } from 'react';
import { Sparkles } from 'lucide-react';
import ChatMessage from './ChatMessage';

export function MessageList({ messages, isLoading, activeTrace, onSelectTrace }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="conversation" aria-live="polite">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          message={message}
          isSelected={activeTrace?.id === message.id}
          onSelectTrace={onSelectTrace}
        />
      ))}

      {isLoading && (
        <div className="message-row assistant">
          <div className="message-avatar assistant">
            <Sparkles size={15} />
          </div>
          <div className="message-content">
            <div className="message-meta">
              <span>DevTrace</span>
              <span className="message-time">traversing graph...</span>
            </div>
            <div className="message-bubble assistant loading-bubble">
              <span />
              <span />
              <span />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}

export default MessageList;
