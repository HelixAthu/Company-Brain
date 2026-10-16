import React, { useState } from 'react';
import {
  Activity,
  Check,
  ChevronRight,
  Code2,
  Copy,
  Database,
  FileText,
  GitBranch,
  Layers3,
  PanelRight,
  Settings2,
  UserRound,
  UsersRound,
  Zap,
} from 'lucide-react';

export function GraphInspector({
  isOpen,
  onToggle,
  activeTrace,
  dbConnected = true,
}) {
  const [copied, setCopied] = useState(false);

  const query = activeTrace?.query || activeTrace?.cypher_query || `MATCH (s:System {name: "Payment Gateway"})<-[:OWNS]-(t:Team) RETURN s, t`;
  
  // Normalize nodes from either array format or backend Pydantic format
  const rawNodes = activeTrace?.traversed_nodes || activeTrace?.nodes || [
    { name: 'Payment Gateway', type: 'System', color: 'violet' },
    { name: 'Payments Team', type: 'Team', color: 'cyan' },
    { name: 'Elena Rostova', type: 'Person', color: 'amber' },
    { name: 'Bob Smith', type: 'Person', color: 'amber' },
  ];

  const nodes = rawNodes.map((item) => {
    if (Array.isArray(item)) {
      return { name: item[0], type: item[1], color: item[2] || 'cyan' };
    }
    const type = item.type || 'System';
    const color =
      type === 'Person' ? 'amber' :
      type === 'Team' ? 'cyan' :
      type === 'System' ? 'violet' :
      type === 'Document' ? 'rose' :
      type === 'Decision' ? 'amber' : 'cyan';
    return {
      name: item.name || item.id || 'Node',
      type,
      color,
      details: item.details || {},
    };
  });

  const path = activeTrace?.path || (
    nodes.length > 1
      ? nodes.map((n) => n.type).filter((v, i, a) => a.indexOf(v) === i).join(' → ')
      : 'System → Team → Person'
  );

  function copyQuery() {
    if (!query) return;
    navigator.clipboard?.writeText(query);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  }

  const highlightTokens = ['MATCH', 'OPTIONAL MATCH', 'RETURN', 'WHERE', 'ORDER BY', 'LIMIT', 'AS', 'WITH', 'COLLECT', 'CONTAINS'];

  return (
    <aside className={`inspector-panel glass-panel ${isOpen ? 'open' : 'closed'}`}>
      <div className="inspector-header">
        <div>
          <div className="eyebrow">
            <span className="eyebrow-line cyan" /> LIVE TRACE
          </div>
          <h2>Graph inspector</h2>
        </div>
        <button
          className="icon-button"
          onClick={onToggle}
          aria-label={isOpen ? 'Collapse inspector' : 'Expand inspector'}
        >
          {isOpen ? <PanelRight size={17} /> : <ChevronRight size={17} />}
        </button>
      </div>

      {isOpen && (
        <>
          <div className="trace-summary">
            <div className="trace-summary-icon">
              <GitBranch size={17} />
            </div>
            <div>
              <strong>Graph Trace Result</strong>
              <span>
                {activeTrace?.execution_time_ms ? `${activeTrace.execution_time_ms}ms · ` : 'Sub-millisecond · '}
                FalkorDB Engine
              </span>
            </div>
            <div className="trace-pulse">
              <span />
            </div>
          </div>

          <div className="inspector-section query-section">
            <div className="section-label">
              <span>
                <Code2 size={14} /> Executed Cypher
              </span>
              <button onClick={copyQuery} type="button">
                {copied ? <Check size={14} /> : <Copy size={14} />}{' '}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <div className="code-window">
              <div className="code-toolbar">
                <span>
                  <i className="window-dot red" />
                  <i className="window-dot yellow" />
                  <i className="window-dot green" />
                </span>
                <span className="code-language">cypher</span>
              </div>
              <pre>
                <code>
                  {query.split('\n').map((line, index) => (
                    <span key={index} className="code-line">
                      <em>{String(index + 1).padStart(2, '0')}</em>
                      <span>
                        {line
                          .replace(
                            new RegExp(`\\b(${highlightTokens.join('|')})\\b`, 'g'),
                            (token) => `§${token}§`
                          )
                          .split('§')
                          .map((part, partIndex) =>
                            highlightTokens.includes(part) ? (
                              <b key={partIndex}>{part}</b>
                            ) : (
                              part
                            )
                          )}
                      </span>
                    </span>
                  ))}
                </code>
              </pre>
            </div>
          </div>

          <div className="inspector-section">
            <div className="section-label">
              <span>
                <Layers3 size={14} /> Traversed entities
              </span>
              <span className="entity-count">{nodes.length} found</span>
            </div>
            <div className="entity-list">
              {nodes.map((node, index) => (
                <div className="entity-row" key={`${node.name}-${index}`}>
                  <span className={`entity-icon ${node.color}`}>
                    {node.type === 'Person' ? (
                      <UserRound size={13} />
                    ) : node.type === 'Team' ? (
                      <UsersRound size={13} />
                    ) : node.type === 'Document' ? (
                      <FileText size={13} />
                    ) : node.type === 'Decision' ? (
                      <Zap size={13} />
                    ) : (
                      <Database size={13} />
                    )}
                  </span>
                  <span className="entity-name">{node.name}</span>
                  <span className="entity-type">{node.type}</span>
                  <ChevronRight size={14} className="entity-chevron" />
                </div>
              ))}
            </div>
          </div>

          <div className="inspector-section relationship-section">
            <div className="section-label">
              <span>
                <GitBranch size={14} /> Relationship path
              </span>
            </div>
            <div className="path-visual">
              {path.split(' → ').map((item, index, array) => (
                <span key={`${item}-${index}`}>
                  <span className="path-node">{item}</span>
                  {index < array.length - 1 && <ChevronRight size={14} />}
                </span>
              ))}
            </div>
          </div>

          <div className="inspector-footer">
            <div className="footer-orb">
              <Activity size={16} />
            </div>
            <div>
              <strong>{dbConnected ? 'FalkorDB cluster active' : 'Connecting to FalkorDB...'}</strong>
              <span>Cypher engine port 6379</span>
            </div>
            <button className="icon-button" type="button" aria-label="Settings">
              <Settings2 size={15} />
            </button>
          </div>
        </>
      )}
    </aside>
  );
}

export default GraphInspector;
