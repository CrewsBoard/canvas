import { NodeModule, NodeRegistry, NodeUiConfig } from '@/types/flowNode.types.ts';

const loadCustomNode = async (nodeUiConfig: NodeUiConfig): Promise<NodeRegistry> => {
    const url = nodeUiConfig.ui_bundle!;
    try {
        const module = await import(/* @vite-ignore */ url);
        const customModule = module.default ?? module;
        await customModule.initialize(nodeUiConfig);
        // @todo need to implement a caching mechanism
        return customModule.nodes;
    } catch (error) {
        console.error(`Failed to load custom flow node from ${url}:`, error);
        return {};
    }
};
const uiComponentLoader: NodeModule = {
    nodes: {},
    initialize: async nodeUiConfigs => {
        console.log('Initializing flow nodes');
        for (const nodeUiConfig of nodeUiConfigs) {
            if (nodeUiConfig.ui_bundle) {
                try {
                    const customNodes = await loadCustomNode(nodeUiConfig);
                    Object.assign(uiComponentLoader.nodes, customNodes);
                } catch (error) {
                    console.error(`Failed to initialize custom flow node ${nodeUiConfig.name}:`, error);
                }
            } else {
                const dirName = nodeUiConfig.name.replace(/_/g, '-');
                const componentName = nodeUiConfig.name
                    .replace(/_/g, '-')
                    .replace(/\b\w/g, char => char.toUpperCase())
                    .replace(/-/g, '');
                const component = `../../flow-nodes/${dirName}/${componentName}.tsx`;
                const importedComponent = await import(/* @vite-ignore */ component);
                const node: NodeRegistry = {
                    [nodeUiConfig.name]: {
                        uiComponent: importedComponent.default,
                    },
                };
                Object.assign(uiComponentLoader.nodes, node);
            }
        }
    },
    cleanup: async () => {
        console.log('Cleaning up flow nodes');
        uiComponentLoader.nodes = {};
    },
};

export default uiComponentLoader;
