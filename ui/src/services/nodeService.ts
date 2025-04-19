/// <reference types="vite/client" />
import { NodeUiConfig } from '../types/flow-node';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fetchNodeTypes = async (): Promise<NodeUiConfig[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/node-types`);
    if (!response.ok) {
      throw new Error('Failed to fetch node types');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching node types:', error);
    return [];
  }
}; 