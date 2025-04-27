import React from "react";
import {NodeComponentProps} from "@/types/flowNode.types.ts";

const OutputNode: React.FC<NodeComponentProps> = ({
                                                      data,
                                                      selected
                                                  }) => {
    return (
        <div className={`node ${selected ? 'selected' : ''}`}
             style={{borderColor: '#FF9800'}}>
            <div className="node-header">
                <h3>{data.title}</h3>
            </div>
            <div className="node-content">
                <p>Output Data: {data?.outputData || 'Not set'}</p>
            </div>
            <div className="node-ports">
                <div className="input-port" data-handleid="success"/>
            </div>
        </div>
    );
};

export default OutputNode;
