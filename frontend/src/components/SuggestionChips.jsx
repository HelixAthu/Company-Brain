import React from 'react';
import { ArrowUpRight, Shield, AlertTriangle, History } from 'lucide-react';

export const DEFAULT_SUGGESTIONS = [
  {
    text: 'Who owns the Payment Gateway?',
    category: 'Ownership',
    icon: Shield,
  },
  {
    text: 'What services break if the Billing DB fails?',
    category: 'Blast Radius',
    icon: AlertTriangle,
  },
  {
    text: 'Why was the legacy cache migrated?',
    category: 'Decisions / ADR',
    icon: History,
  },
];

export function SuggestionChips({ suggestions = DEFAULT_SUGGESTIONS, onSelectSuggestion, isLoading }) {
  return (
    <div className="suggestion-row">
      <span className="suggestion-label">Try asking</span>
      {suggestions.map((item, index) => {
        const text = typeof item === 'string' ? item : item.text;
        const IconComponent = typeof item === 'object' && item.icon ? item.icon : null;

        return (
          <button
            key={index}
            className="suggestion-chip"
            onClick={() => onSelectSuggestion && onSelectSuggestion(text)}
            disabled={isLoading}
            type="button"
          >
            {IconComponent && <IconComponent size={12} className="suggestion-chip-icon" />}
            <span>{text}</span>
            <ArrowUpRight size={13} />
          </button>
        );
      })}
    </div>
  );
}

export default SuggestionChips;
