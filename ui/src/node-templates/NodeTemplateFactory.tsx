import React, { ComponentType, LazyExoticComponent, Suspense, useMemo } from 'react';

const modules = import.meta.glob('@/node-templates/**/*.tsx');

type ModuleType = {
    [key: string]: () => Promise<{ default: ComponentType<unknown> }>;
};

const NodeTemplateFactory: React.FC<{
    type: string;
    [key: string]: unknown;
}> = ({ type, ...props }) => {
    const Component = useMemo<LazyExoticComponent<ComponentType<unknown>> | null>(() => {
        let foundModule = null;
        for (const path in modules) {
            if (path.includes(type)) {
                foundModule = modules[path];
                break;
            }
        }

        if (foundModule) {
            return React.lazy(foundModule as ModuleType[string]);
        }
        return null;
    }, [type]);

    if (!Component) {
        return <div>Component "{type}" not found</div>;
    }

    return (
        <Suspense fallback={<div>Loading...</div>}>
            <Component {...props} />
        </Suspense>
    );
};

export default NodeTemplateFactory;
