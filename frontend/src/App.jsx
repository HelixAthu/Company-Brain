import { useEffect, useRef, useState } from 'react';
import {
  Activity,
  ArrowUpRight,
  Bot,
  Check,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  Clock3,
  Code2,
  Copy,
  Database,
  FileText,
  GitBranch,
  Globe2,
  Layers3,
  Menu,
  MessageSquareText,
  Network,
  PanelRight,
  Plus,
  Search,
  Send,
  Settings2,
  Sparkles,
  Terminal,
  UserRound,
  UsersRound,
  X,
  Zap,
} from 'lucide-react';

const suggestions = [
  'Who owns the Payment Gateway?',
  'What services break if the Billing DB fails?',
  'Why was the legacy cache migrated?',
];

const demoResponses = {
  'Who owns the Payment Gateway?': {
    answer: 'The Payment Gateway is owned by the **Payments Platform** team. **Maya Chen** is the primary technical owner, with **Jordan Ellis** as the product counterpart.',
    meta: '3 entities · 1 relationship',
    query: `MATCH (s:System {name: "Payment Gateway"})
MATCH (s)-[:OWNED_BY]->(t:Team)
MATCH (t)-[:HAS_MEMBER]->(p:Person)
RETURN s, t, p`,
    nodes: [
      ['Payment Gateway', 'System', 'violet'],
      ['Payments Platform', 'Team', 'cyan'],
      ['Maya Chen', 'Person', 'amber'],
      ['Jordan Ellis', 'Person', 'amber'],
    ],
    path: 'System → Team → Person',
  },
  'What services break if the Billing DB fails?': {
    answer: 'A Billing DB outage impacts **Invoice Service**, **Subscription API**, and **Revenue Dashboard**. Checkout can still authorize payments, but recurring billing and invoice generation will queue until the database recovers.',
    meta: '5 entities · 6 relationships',
    query: `MATCH (db:System {name: "Billing DB"})
MATCH (service:System)-[:DEPENDS_ON]->(db)
OPTIONAL MATCH (service)-[:DOCUMENTED_BY]->(doc:Document)
RETURN service, doc`,
    nodes: [
      ['Billing DB', 'System', 'violet'],
      ['Invoice Service', 'System', 'cyan'],
      ['Subscription API', 'System', 'cyan'],
      ['Revenue Dashboard', 'System', 'cyan'],
      ['Billing Runbook', 'Document', 'rose'],
    ],
    path: 'System → System → Document',
  },
  'Why was the legacy cache migrated?': {
    answer: 'The legacy cache was migrated to **Edge Cache** in Q3 2024 to reduce regional latency and remove a single-zone failure mode. The decision record cites a **42% p95 latency reduction** in the first month.',
    meta: '4 entities · 4 relationships',
    query: `MATCH (old:System {name: "Legacy Cache"})
MATCH (old)-[:REPLACED_BY]->(new:System)
MATCH (d:Decision)-[:ABOUT]->(old)
RETURN old, new, d`,
    nodes: [
      ['Legacy Cache', 'System', 'violet'],
      ['Edge Cache', 'System', 'cyan'],
      ['Cache Modernization', 'Decision', 'amber'],
      ['Platform Architecture', 'Team', 'rose'],
    ],
    path: 'System → Decision → Team',
  },
};

const initialMessages = [
  {
    id: 1,
    role: 'assistant',
    text: 'Hey, I\'m DevTrace. Ask me anything about your systems, teams, and the decisions behind them.',
    time: '09:41 AM',
    meta: 'Ready to trace your company graph',
  },
  {
    id: 2,
    role: 'user',
    text: 'Give me a quick read on our payments stack.',
    time: '09:42 AM',
  },
  {
    id: 3,
    role: 'assistant',
    text: 'Your payments stack centers on **Payment Gateway**, owned by Payments Platform. It connects to the Billing DB and emits events to Ledger Service. The most recent architecture decision was the regional failover rollout in June.',
    time: '09:42 AM',
    meta: '4 entities · 5 relationships',
    query: `MATCH path=(s:System {domain: "payments"})-[*1..2]->(n)
RETURN path
ORDER BY s.updatedAt DESC`,
    nodes: [
      ['Payment Gateway', 'System', 'violet'],
      ['Payments Platform', 'Team', 'cyan'],
      ['Billing DB', 'System', 'cyan'],
      ['Regional Failover', 'Decision', 'amber'],
    ],
    path: 'System → Team → System → Decision',
  },
];

function formatText(text) {
  return text.split(/(\*\*.*?\*\*)/g).map((part, index) =>
    part.startsWith('**') ? <strong key={index}>{part.slice(2, -2)}</strong> : part,
  );
}

function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [inspectorOpen, setInspectorOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [fallbackMode, setFallbackMode] = useState(true);
  const [activeTrace, setActiveTrace] = useState(initialMessages[2]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  async function askQuestion(question) {
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || isLoading) return;

    const userMessage = { id: Date.now(), role: 'user', text: trimmedQuestion, time: 'Now' };
    setMessages((current) => [...current, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      if (!fallbackMode) {
        const response = await fetch('http://localhost:8000/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: trimmedQuestion }),
        });
        if (!response.ok) throw new Error('API unavailable');
        const data = await response.json();
        const apiMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          text: data.answer ?? data.response ?? 'The graph returned no explanation for this query.',
          time: 'Now',
          meta: data.meta ?? 'Live API response',
          query: data.cypher ?? data.query,
          nodes: data.nodes,
          path: data.path,
        };
        setMessages((current) => [...current, apiMessage]);
        setActiveTrace(apiMessage);
      } else {
        await new Promise((resolve) => setTimeout(resolve, 850));
        const matched = Object.entries(demoResponses).find(([prompt]) =>
          trimmedQuestion.toLowerCase().includes(prompt.toLowerCase().slice(0, 18)),
        )?.[1] ?? demoResponses['Who owns the Payment Gateway?'];
        const assistantMessage = { id: Date.now() + 1, role: 'assistant', text: matched.answer, time: 'Now', ...matched };
        setMessages((current) => [...current, assistantMessage]);
        setActiveTrace(assistantMessage);
      }
    } catch {
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        text: 'I could not reach the Company Brain API. I kept your question here so you can retry when the backend is ready.',
        time: 'Now',
        meta: 'Connection interrupted',
      };
      setMessages((current) => [...current, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  function startNewTrace() {
    setMessages([initialMessages[0]]);
    setActiveTrace(initialMessages[2]);
    setInput('');
  }

  function copyQuery() {
    if (!activeTrace?.query) return;
    navigator.clipboard?.writeText(activeTrace.query);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  }

  return (
    <main className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />
      <div className="ambient ambient-three" />
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark"><Network size={17} strokeWidth={2.4} /></div>
          <div>
            <div className="brand-name">DevTrace</div>
            <div className="brand-subtitle">Company Brain</div>
          </div>
        </div>

        <div className="header-center">
          <div className="connection-status"><span className="status-dot" /> FalkorDB Connected</div>
          <span className="header-divider" />
          <span className="workspace-label"><span className="workspace-dot" /> acme-platform / production</span>
        </div>

        <nav className="top-actions">
          <button className="icon-button mobile-menu-button" aria-label="Open navigation" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}><Menu size={18} /></button>
          <a href="#activity"><Clock3 size={15} /> Activity</a>
          <a href="#docs"><CircleHelp size={15} /> Docs</a>
          <button className="avatar" aria-label="Open account menu">AR</button>
        </nav>
        {mobileMenuOpen && <div className="mobile-nav"><a href="#activity">Activity</a><a href="#docs">Docs</a></div>}
      </header>

      <div className="workspace">
        <section className="chat-panel glass-panel">
          <div className="panel-heading">
            <div>
              <div className="eyebrow"><span className="eyebrow-line" /> TRACE CONSOLE</div>
              <h1>Ask your company brain<span className="heading-dot">.</span></h1>
              <p className="panel-description">Understand the systems, people, and decisions behind your codebase.</p>
            </div>
            <button className="new-trace-button" onClick={startNewTrace}><Plus size={16} /> New trace</button>
          </div>

          <div className="suggestion-row">
            <span className="suggestion-label">Try asking</span>
            {suggestions.map((suggestion) => <button key={suggestion} className="suggestion-chip" onClick={() => askQuestion(suggestion)}>{suggestion}<ArrowUpRight size={13} /></button>)}
          </div>

          <div className="conversation" aria-live="polite">
            {messages.map((message) => (
              <div key={message.id} className={`message-row ${message.role}`}>
                <div className={`message-avatar ${message.role}`}>
                  {message.role === 'assistant' ? <Sparkles size={15} /> : <UserRound size={15} />}
                </div>
                <div className="message-content">
                  <div className="message-meta"><span>{message.role === 'assistant' ? 'DevTrace' : 'You'}</span><span className="message-time">{message.time}</span></div>
                  <div className={`message-bubble ${message.role}`} onClick={() => message.query && setActiveTrace(message)}>{formatText(message.text)}</div>
                  {message.meta && <div className="message-foot"><Check size={13} /> {message.meta}{message.query && <button onClick={() => setActiveTrace(message)}>View trace <ChevronRight size={12} /></button>}</div>}
                </div>
              </div>
            ))}
            {isLoading && <div className="message-row assistant"><div className="message-avatar assistant"><Sparkles size={15} /></div><div className="message-content"><div className="message-meta"><span>DevTrace</span><span className="message-time">thinking</span></div><div className="message-bubble assistant loading-bubble"><span /><span /><span /></div></div></div>}
            <div ref={bottomRef} />
          </div>

          <div className="composer-wrap">
            <div className="composer">
              <div className="composer-leading"><Search size={18} /></div>
              <input value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && askQuestion(input)} placeholder="Ask about your company graph..." aria-label="Ask about your company graph" />
              <div className="composer-actions"><span className="shortcut">⌘ ↵</span><button className="send-button" onClick={() => askQuestion(input)} disabled={!input.trim() || isLoading} aria-label="Send question"><Send size={16} /></button></div>
            </div>
            <div className="composer-footer"><span><Zap size={12} /> Answers are grounded in your indexed company graph</span><label className="fallback-toggle"><input type="checkbox" checked={fallbackMode} onChange={(event) => setFallbackMode(event.target.checked)} /><span className="toggle-track" /><span>Demo mode</span></label></div>
          </div>
        </section>

        <aside className={`inspector-panel glass-panel ${inspectorOpen ? 'open' : 'closed'}`}>
          <div className="inspector-header"><div><div className="eyebrow"><span className="eyebrow-line cyan" /> LIVE TRACE</div><h2>Graph inspector</h2></div><button className="icon-button" onClick={() => setInspectorOpen(!inspectorOpen)} aria-label={inspectorOpen ? 'Collapse inspector' : 'Expand inspector'}>{inspectorOpen ? <PanelRight size={17} /> : <ChevronRight size={17} />}</button></div>
          {inspectorOpen && <>
            <div className="trace-summary"><div className="trace-summary-icon"><GitBranch size={17} /></div><div><strong>Payment stack trace</strong><span>Updated just now · 46ms</span></div><div className="trace-pulse"><span /></div></div>
            <div className="inspector-section query-section"><div className="section-label"><span><Code2 size={14} /> Generated Cypher</span><button onClick={copyQuery}>{copied ? <Check size={14} /> : <Copy size={14} />} {copied ? 'Copied' : 'Copy'}</button></div><div className="code-window"><div className="code-toolbar"><span><i className="window-dot red" /><i className="window-dot yellow" /><i className="window-dot green" /></span><span className="code-language">cypher</span></div><pre><code>{(activeTrace?.query ?? initialMessages[2].query).split('\n').map((line, index) => <span key={index} className="code-line"><em>{String(index + 1).padStart(2, '0')}</em><span>{line.replace(/(MATCH|RETURN|OPTIONAL MATCH|ORDER BY)/g, (token) => `§${token}§`).split('§').map((part, partIndex) => ['MATCH', 'RETURN', 'OPTIONAL MATCH', 'ORDER BY'].includes(part) ? <b key={partIndex}>{part}</b> : part)}</span></span>)}</code></pre></div></div>
            <div className="inspector-section"><div className="section-label"><span><Layers3 size={14} /> Traversed entities</span><span className="entity-count">{activeTrace?.nodes?.length ?? 4} found</span></div><div className="entity-list">{(activeTrace?.nodes ?? initialMessages[2].nodes).map(([name, type, color]) => <div className="entity-row" key={name}><span className={`entity-icon ${color}`}>{type === 'Person' ? <UserRound size={13} /> : type === 'Team' ? <UsersRound size={13} /> : type === 'Document' ? <FileText size={13} /> : type === 'Decision' ? <Zap size={13} /> : <Database size={13} />}</span><span className="entity-name">{name}</span><span className="entity-type">{type}</span><ChevronRight size={14} className="entity-chevron" /></div>)}</div></div>
            <div className="inspector-section relationship-section"><div className="section-label"><span><GitBranch size={14} /> Relationship path</span></div><div className="path-visual">{(activeTrace?.path ?? 'System → Team → System → Decision').split(' → ').map((item, index, array) => <span key={`${item}-${index}`}><span className="path-node">{item}</span>{index < array.length - 1 && <ChevronRight size={14} />}</span>)}</div></div>
            <div className="inspector-footer"><div className="footer-orb"><Activity size={16} /></div><div><strong>Graph health is good</strong><span>18,402 nodes · 54,821 edges</span></div><button className="icon-button"><Settings2 size={15} /></button></div>
          </>}
        </aside>
      </div>
      <footer className="statusbar"><span><span className="status-dot small" /> All systems operational</span><span>Last indexed 4 min ago</span><span className="statusbar-right"><Code2 size={14} /> v0.8.4 <Globe2 size={14} /> US East</span></footer>
    </main>
  );
}

export default App;
