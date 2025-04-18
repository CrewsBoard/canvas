import React, { createContext, useState, ReactNode } from 'react';

export interface DnDContextType {
  draggedType: string | null;
  setDraggedType: React.Dispatch<React.SetStateAction<string | null>>;
}

const defaultContextValue: DnDContextType = {
  draggedType: null,
  setDraggedType: () => {}, // No-op function as default
};

export const DnDContext = createContext<DnDContextType>(defaultContextValue);

interface DnDProviderProps {
  children: ReactNode;
}

export const DnDProvider = ({ children }: DnDProviderProps) => {
  const [draggedType, setDraggedType] = useState<string | null>(null);

  return (
    <DnDContext.Provider value={{ draggedType, setDraggedType }}>
      {children}
    </DnDContext.Provider>
  );
};
