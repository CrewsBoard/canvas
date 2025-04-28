import React from "react";
import {NodeComponentProps} from "@/types/flowNode.types.ts";

const CrewaiCrewNode: React.FC<NodeComponentProps> = ({data, selected}) => {
    return (
        <div className={`node ${selected ? 'selected' : ''}`}
             style={{borderColor: '#9C27B0'}}>
            <div className="node-header">
                <h3>{data.title}</h3>
            </div>
            <div className="node-content">
                <p>Crew Node</p>
            </div>
            <div className="node-ports">
                <div className="input-port" data-handleid="success"/>
                <div className="output-port" data-handleid="success"/>
            </div>
        </div>
    );
};

export default CrewaiCrewNode;
