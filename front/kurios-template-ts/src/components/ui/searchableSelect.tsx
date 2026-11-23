import { Check, ChevronDown, Search, X } from 'lucide-react';
import React, { useEffect, useMemo, useRef, useState } from 'react';

export interface SelectOption {
  value: string;
  label: string;
}

interface SearchableSelectProps {
  label: string;
  options: SelectOption[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  error?: string;
  disabled?: boolean;
}

export const SearchableSelect: React.FC<SearchableSelectProps> = ({
  label,
  options,
  value,
  onChange,
  placeholder = 'Seleccionar...',
  searchPlaceholder = 'Buscar...',
  error,
  disabled = false,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const selectedOption = useMemo(
    () => options.find((opt) => opt.value === value),
    [options, value]
  );

  // Normaliza tildes y mayúsculas para búsquedas en español
  const filteredOptions = useMemo(() => {
    const normalize = (str: string) =>
      str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

    const term = normalize(searchTerm);
    return options.filter((opt) => normalize(opt.label).includes(term));
  }, [options, searchTerm]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleToggleOpen = () => {
    if (disabled) return;
    setIsOpen((prev) => {
      const nextState = !prev;
      if (nextState) {
        setSearchTerm('');
        requestAnimationFrame(() => inputRef.current?.focus());
      }
      return nextState;
    });
  };

  const handleSelect = (optionValue: string) => {
    onChange(optionValue);
    setIsOpen(false);
    setSearchTerm('');
  };

  return (
    <div className="relative w-full" ref={containerRef}>
      <label className="block text-xs font-medium text-slate-700 mb-1.5">
        {label}
      </label>

      <button
        type="button"
        disabled={disabled}
        onClick={handleToggleOpen}
        className={`w-full flex items-center justify-between px-3 py-2 text-sm rounded-lg border bg-white text-left transition-colors focus:outline-none focus:ring-2 ${
          error
            ? 'border-red-500 focus:ring-red-500/20'
            : 'border-slate-300 hover:border-slate-400 focus:border-indigo-600 focus:ring-indigo-600/20'
        } ${disabled ? 'opacity-50 cursor-not-allowed bg-slate-50' : 'cursor-pointer'}`}
      >
        <span className={`truncate ${selectedOption ? 'text-slate-900' : 'text-slate-400'}`}>
          {selectedOption ? selectedOption.label : placeholder}
        </span>

        <div className="flex items-center gap-1.5 ml-2 shrink-0">
          {value && !disabled && (
            <span
              role="button"
              tabIndex={0}
              onClick={(e) => {
                e.stopPropagation();
                onChange('');
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  e.stopPropagation();
                  onChange('');
                }
              }}
              className="p-0.5 text-slate-400 hover:text-slate-700 rounded"
            >
              <X className="w-3.5 h-3.5" />
            </span>
          )}
          <ChevronDown
            className={`w-4 h-4 text-slate-500 transition-transform duration-150 ${
              isOpen ? 'rotate-180' : ''
            }`}
          />
        </div>
      </button>

      {isOpen && (
        <div className="absolute z-50 mt-1.5 w-full rounded-lg border border-slate-200 bg-white overflow-hidden">
          <div className="p-2 border-b border-slate-100 flex items-center gap-2 bg-slate-50">
            <Search className="w-4 h-4 text-slate-400 shrink-0" />
            <input
              ref={inputRef}
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder={searchPlaceholder}
              className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 focus:outline-none"
            />
          </div>

          <ul className="max-h-48 overflow-y-auto py-1 divide-y divide-slate-100">
            {filteredOptions.length === 0 ? (
              <li className="px-3 py-2.5 text-xs text-slate-500 text-center">
                No se encontraron resultados
              </li>
            ) : (
              filteredOptions.map((option) => {
                const isSelected = option.value === value;
                return (
                  <li key={option.value}>
                    <button
                      type="button"
                      onClick={() => handleSelect(option.value)}
                      className={`w-full flex items-center justify-between px-3 py-2 text-sm text-left transition-colors ${
                        isSelected
                          ? 'bg-indigo-50 text-indigo-700 font-medium'
                          : 'text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <span className="truncate">{option.label}</span>
                      {isSelected && <Check className="w-4 h-4 text-indigo-600 shrink-0 ml-2" />}
                    </button>
                  </li>
                );
              })
            )}
          </ul>
        </div>
      )}

      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  );
};