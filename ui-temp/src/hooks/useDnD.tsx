import { useContext } from 'react';

import { DnDContext, DnDContextType } from '@/contexts/DnDContext';
export const useDnD = (): DnDContextType => {
  const context = useContext(DnDContext);
  if (context === undefined) {
    throw new Error('useDnD must be used within a DnDProvider');
  }
  return context;
};
