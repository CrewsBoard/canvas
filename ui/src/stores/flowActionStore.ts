import { create } from 'zustand';

import { FlowActionState } from '@/types/stores.types.ts';

export const useFlowActionStore = create<FlowActionState>(set => ({
    showEditor: false,
    setShowEditor: showEditor => set({ showEditor }),
    toggleEditor: () => set(state => ({ showEditor: !state.showEditor })),
}));
