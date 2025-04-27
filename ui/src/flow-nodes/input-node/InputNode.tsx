import React from "react";
import {NodeComponentProps} from "@/types/flowNode.types.ts";

const InputNode: React.FC<NodeComponentProps> = ({data, selected}) => {
    return (
        <div className={`node ${selected ? 'selected' : ''}`}
             style={{borderColor: '#4CAF50'}}>
            <div className="node-header">
                <h3>{data.title}</h3>
            </div>
            <div className="node-content">
                <p>Input Data: {data?.inputData || 'Not set'}</p>
            </div>
            <div className="node-ports">
                <div className="output-port" data-handleid="success"/>
            </div>
        </div>
    );
};

export default InputNode;
