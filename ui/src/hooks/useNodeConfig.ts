import { useState, useEffect } from 'react';
import { NodeUIConfig } from '../types/flow-node';

export const useNodeConfig = (nodeType: string) => {
  const [config, setConfig] = useState<NodeUIConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await fetch('/api/node-types');
        const nodeTypes = await response.json();
        const nodeConfig = nodeTypes.find((type: any) => type.type === nodeType);
        if (nodeConfig) {
          setConfig(nodeConfig);
        } else {
          setError(`Node type ${nodeType} not found`);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch node config');
      } finally {
        setLoading(false);
      }
    };

    fetchConfig();
  }, [nodeType]);

  return { config, loading, error };
}; 