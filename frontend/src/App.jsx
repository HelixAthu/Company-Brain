import React, { useState, useEffect } from 'react';
import {
  Clock3,
  CircleHelp,
  Code2,
  Globe2,
  Menu,
  Network,
  Plus,
  Search,
  Send,
  Zap,
  PlayCircle,
  Radio,
} from 'lucide-react';
import { askQuestion, checkHealth } from './services/api';
import MessageList from './components/MessageList';
import SuggestionChips from './components/SuggestionChips';
import GraphInspector from './components/GraphInspector';

const initialMessages = [
  {
    id: 1,
    role: 'assistant',
    text: "Hey, I'm **DevTrace**. Ask me anything about your systems, teams, dependencies, and architecture decisions.",
    time: '09:41 AM',
    meta: 'Ready to trace your company graph',
  },
  {
    id: 2,
    role: 'user',
    text: 'Who owns the Payment Gateway?',
    time: '09:42 AM',
  },
  {
    id: 3,
    role: 'assistant',
    text: 'The **Payment Gateway API** (Tier-1) is owned by the **Payments Team** (`#team-payments`). **Elena Rostova** is the Staff Architect and **Bob Smith** is the senior on-call engineer.',
    time: '09:42 AM',
    meta: '4 entities · 1 relationship',
    execution_time_ms: 3.4,
    query: `MATCH (s:System {name: 'Payment Gateway'})<-[own:OWNS]-(t:Team)<-[mem:MEMBER_OF]-(p:Person)
OPTIONAL MATCH (doc:Document)-[:DOCUMENTS]->(s)
RETURN s.name AS system, t.name AS team, t.slack_channel AS slack, collect(p.name) AS engineers, doc.title AS runbook`,
    traversed_nodes: [
      { name: 'Payment Gateway', type: 'System', color: 'violet' },
      { name: 'Payments Team', type: 'Team', color: 'cyan' },
      { name: 'Elena Rostova', type: 'Person', color: 'amber' },
      { name: 'Bob Smith', type: 'Person', color: 'amber' },
    ],
    citations: [
      {
        title: 'Payment Gateway Incident Runbook & Disaster Recovery',
        url: 'https://wiki.company.internal/runbooks/payment-gateway',
        type: 'Runbook',
      },
    ],
    path: 'System → Team → Person',
  },
];

function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [inspectorOpen, setInspectorOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [fallbackMode, setFallbackMode] = useState(false);
  const [activeTrace, setActiveTrace] = useState(initialMessages[2]);
  const [dbConnected, setDbConnected] = useState(true);

  // Real-time FalkorDB connection polling hook
  useEffect(() => {
    let isMounted = true;

    async function pollHealth() {
      try {
        const health = await checkHealth();
        if (isMounted) {
          setDbConnected(health.falkordb_connected ?? true);
        }
      } catch (err) {
        if (isMounted) {
          setDbConnected(false);
        }
      }
    }

    pollHealth();
    const interval = setInterval(pollHealth, 10000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  async function handleSendQuestion(questionText) {
    const trimmed = (questionText || input).trim();
    if (!trimmed || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      text: trimmed,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await askQuestion(trimmed, fallbackMode);

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        text: data.answer || 'Query executed against company graph.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        meta: `${data.traversed_nodes?.length || 0} entities traversed`,
        execution_time_ms: data.execution_time_ms,
        query: data.cypher_query,
        traversed_nodes: data.traversed_nodes,
        citations: data.citations || [],
        path: data.traversed_nodes?.map((n) => n.type).filter((v, i, a) => a.indexOf(v) === i).join(' → ') || 'System → Team',
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setActiveTrace(assistantMessage);
    } catch (err) {
      console.warn('Backend request failed, falling back to local demo resolution:', err);
      const fallbackReply = {
        id: Date.now() + 1,
        role: 'assistant',
        text: `### FalkorDB Graph Traversal\nQuery resolved for: **"${trimmed}"**.\n\n*Note: Connected to local demo fallback.*`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        meta: 'Demo fallback trace',
        execution_time_ms: 4.2,
        query: `MATCH (s:System) WHERE toLower(s.name) CONTAINS toLower("${trimmed.slice(0, 15)}") RETURN s LIMIT 5`,
        traversed_nodes: [
          { name: trimmed.slice(0, 20), type: 'System', color: 'violet' },
          { name: 'Core Infra', type: 'Team', color: 'cyan' },
        ],
        path: 'System → Team',
      };
      setMessages((prev) => [...prev, fallbackReply]);
      setActiveTrace(fallbackReply);
    } finally {
      setIsLoading(false);
    }
  }

  function startNewTrace() {
    setMessages([initialMessages[0]]);
    setActiveTrace(initialMessages[2]);
    setInput('');
  }

  return (
    <main className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />
      <div className="ambient ambient-three" />

      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark">
            <Network size={17} strokeWidth={2.4} />
          </div>
          <div>
            <div className="brand-name">DevTrace</div>
            <div className="brand-subtitle">Company Brain</div>
          </div>
        </div>

        <div className="header-center">
          <div className="connection-status">
            <span className={`status-dot ${dbConnected ? 'connected' : 'disconnected'}`} />
            <span className={dbConnected ? 'status-text' : 'status-text offline'}>
              {dbConnected ? 'FalkorDB Connected' : 'FalkorDB Offline (Demo Active)'}
            </span>
          </div>
          <span className="header-divider" />
          <span className="workspace-label">
            <span className="workspace-dot" /> acme-platform / production
          </span>
          <span className="header-divider" />
          
          {/* Topbar Demo Mode Switch */}
          <div className="header-demo-toggle">
            <button
              type="button"
              className={`demo-pill ${fallbackMode ? 'active' : ''}`}
              onClick={() => setFallbackMode(!fallbackMode)}
              title="Toggle between live FalkorDB/Gemini execution and pre-computed demo resilience"
            >
              {fallbackMode ? <PlayCircle size={13} /> : <Radio size={13} />}
              <span>{fallbackMode ? 'Demo Mode Active' : 'Live Graph Mode'}</span>
            </button>
          </div>
        </div>

        <nav className="top-actions">
          <button
            className="icon-button mobile-menu-button"
            aria-label="Open navigation"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Menu size={18} />
          </button>
          <a href="#activity">
            <Clock3 size={15} /> Activity
          </a>
          <a href="#docs">
            <CircleHelp size={15} /> Docs
          </a>
          <button className="avatar" aria-label="Open account menu">
            AR
          </button>
        </nav>
        {mobileMenuOpen && (
          <div className="mobile-nav">
            <a href="#activity">Activity</a>
            <a href="#docs">Docs</a>
            <button
              className="mobile-demo-btn"
              onClick={() => setFallbackMode(!fallbackMode)}
            >
              {fallbackMode ? 'Switch to Live Mode' : 'Switch to Demo Mode'}
            </button>
          </div>
        )}
      </header>

      <div className="workspace">
        <section className="chat-panel glass-panel">
          <div className="panel-heading">
            <div>
              <div className="eyebrow">
                <span className="eyebrow-line" /> TRACE CONSOLE
              </div>
              <h1>
                Ask your company brain<span className="heading-dot">.</span>
              </h1>
              <p className="panel-description">
                Understand the systems, people, and architectural decisions behind your codebase.
              </p>
            </div>
            <button className="new-trace-button" onClick={startNewTrace}>
              <Plus size={16} /> New trace
            </button>
          </div>

          <SuggestionChips
            onSelectSuggestion={handleSendQuestion}
            isLoading={isLoading}
          />

          <MessageList
            messages={messages}
            isLoading={isLoading}
            activeTrace={activeTrace}
            onSelectTrace={(msg) => setActiveTrace(msg)}
          />

          <div className="composer-wrap">
            <div className="composer">
              <div className="composer-leading">
                <Search size={18} />
              </div>
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendQuestion(input)}
                placeholder="Ask about your company graph (e.g., who owns Payment Gateway?)..."
                aria-label="Ask about your company graph"
                disabled={isLoading}
              />
              <div className="composer-actions">
                <span className="shortcut">↵</span>
                <button
                  className="send-button"
                  onClick={() => handleSendQuestion(input)}
                  disabled={!input.trim() || isLoading}
                  aria-label="Send question"
                >
                  <Send size={16} />
                </button>
              </div>
            </div>
            <div className="composer-footer">
              <span>
                <Zap size={12} /> Answers are grounded in your indexed FalkorDB graph
              </span>
              <label className="fallback-toggle">
                <input
                  type="checkbox"
                  checked={fallbackMode}
                  onChange={(e) => setFallbackMode(e.target.checked)}
                />
                <span className="toggle-track" />
                <span>Demo mode</span>
              </label>
            </div>
          </div>
        </section>

        <GraphInspector
          isOpen={inspectorOpen}
          onToggle={() => setInspectorOpen(!inspectorOpen)}
          activeTrace={activeTrace}
          dbConnected={dbConnected}
        />
      </div>

      <footer className="statusbar">
        <span>
          <span className="status-dot small" /> All systems operational
        </span>
        <span>Graph indexed · FalkorDB v1.0.8</span>
        <span className="statusbar-right">
          <Code2 size={14} /> DevTrace v1.0.0-hackathon <Globe2 size={14} /> Production
        </span>
      </footer>
    </main>
  );
}

export default App;
