import { NodeUIConfig } from '../types/flow-node';

const API_BASE_URL = 'http://localhost:8001'; // Update this with your actual API URL

export const fetchNodeTypes = async (): Promise<NodeUIConfig[]> => {
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