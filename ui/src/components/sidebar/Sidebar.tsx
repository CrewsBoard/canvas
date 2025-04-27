import React from 'react';
import {SidebarProps} from "@/components/sidebar/sidebarProps.types.ts";

const Sidebar: React.FC<SidebarProps> = ({nodeTypes, onDragStart}) => {
    return (
        <div className="sidebar" style={{
            position: 'absolute',
            left: 0,
            top: 0,
            bottom: 0,
            width: '200px',
            background: 'rgba(255, 255, 255, 0.8)',
            backdropFilter: 'blur(4px)',
            borderRight: '1px solid #e2e8f0',
            padding: '15px',
            zIndex: 4,
            overflowY: 'auto'
        }}>
            <h3 style={{
                margin: '0 0 10px 0',
                paddingBottom: '10px',
                borderBottom: '1px solid #e2e8f0',
                fontSize: '14px',
                fontWeight: 500,
                color: '#4a5568'
            }}>
                Available Nodes
            </h3>
            <div style={{display: 'flex', flexDirection: 'column', gap: '8px'}}>
                {Object.entries(nodeTypes).map(([type, def]) => (
                    <div
                        key={type}
                        draggable
                        onDragStart={(e) => onDragStart(e, type)}
                        style={{
                            padding: '8px 12px',
                            background: 'white',
                            border: '1px solid #e2e8f0',
                            borderRadius: '4px',
                            cursor: 'grab',
                            fontSize: '12px',
                            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
                            transition: 'all 0.2s ease'
                        }}
                        onMouseOver={(e) => {
                            e.currentTarget.style.transform = 'translateX(2px)';
                            e.currentTarget.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
                        }}
                        onMouseOut={(e) => {
                            e.currentTarget.style.transform = 'translateX(0)';
                            e.currentTarget.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.05)';
                        }}
                    >
                        <div style={{
                            fontWeight: 500,
                            color: '#2d3748'
                        }}>{def.name || type}</div>
                        {def.description && (
                            <div style={{
                                fontSize: '11px',
                                color: '#718096',
                                marginTop: '4px'
                            }}>{def.description}</div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Sidebar; 
