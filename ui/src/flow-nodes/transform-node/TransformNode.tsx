import React from "react";
import {NodeComponentProps} from "@/types/flowNode.types.ts";

const TransformNode: React.FC<NodeComponentProps> = ({
                                                         data,
                                                         selected
                                                     }) => {
    return (
        <div className={`node ${selected ? 'selected' : ''}`}
             style={{borderColor: '#2196F3'}}>
            <div className="node-header">
                <h3>{data.title}</h3>
            </div>
            <div className="node-content">
                <p>Transformations: {data?.transformations ? 'Configured' : 'Not set'}</p>
            </div>
            <div className="node-ports">
                <div className="input-port" data-handleid="success"/>
                <div className="output-port" data-handleid="success"/>
                <div className="output-port" data-handleid="failure"/>
            </div>
        </div>
    );
};

export default TransformNode;
