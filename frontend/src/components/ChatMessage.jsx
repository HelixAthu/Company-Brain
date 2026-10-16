import React from 'react';
import { Sparkles, UserRound, Check, ChevronRight, FileText, ExternalLink, Clock } from 'lucide-react';

function formatText(text) {
  if (!text) return '';
  return text.split(/(\*\*.*?\*\*)/g).map((part, index) =>
    part.startsWith('**') ? <strong key={index}>{part.slice(2, -2)}</strong> : part
  );
}

export function ChatMessage({ message, onSelectTrace, isSelected }) {
  const isAssistant = message.role === 'assistant';

  return (
    <div className={`message-row ${message.role} ${isSelected ? 'selected-trace' : ''}`}>
      <div className={`message-avatar ${message.role}`}>
        {isAssistant ? <Sparkles size={15} /> : <UserRound size={15} />}
      </div>
      <div className="message-content">
        <div className="message-meta">
          <span>{isAssistant ? 'DevTrace' : 'You'}</span>
          <span className="message-time">{message.time || 'Now'}</span>
          {message.execution_time_ms && (
            <span className="execution-badge">
              <Clock size={10} style={{ display: 'inline', marginRight: 3 }} />
              {message.execution_time_ms}ms · FalkorDB
            </span>
          )}
        </div>

        <div
          className={`message-bubble ${message.role}`}
          onClick={() => (message.query || message.cypher_query) && onSelectTrace && onSelectTrace(message)}
        >
          {formatText(message.text || message.answer)}
        </div>

        {/* Citations badges if present */}
        {message.citations && message.citations.length > 0 && (
          <div className="message-citations">
            <span className="citation-label">Sources:</span>
            {message.citations.map((c, i) => (
              <a
                key={i}
                href={c.url || '#'}
                target="_blank"
                rel="noreferrer"
                className="citation-pill"
                onClick={(e) => !c.url && e.preventDefault()}
              >
                <FileText size={11} />
                <span>{c.title}</span>
                {c.url && <ExternalLink size={10} />}
              </a>
            ))}
          </div>
        )}

        {(message.meta || message.query || message.cypher_query) && (
          <div className="message-foot">
            <Check size={13} /> {message.meta || 'Grounded in graph data'}
            {(message.query || message.cypher_query) && (
              <button
                className="view-trace-link"
                onClick={() => onSelectTrace && onSelectTrace(message)}
              >
                View trace <ChevronRight size={12} />
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
