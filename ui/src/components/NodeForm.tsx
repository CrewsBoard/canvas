import React, { useState } from 'react';
import { NodeUiFields } from '../types/flow-node';

interface NodeFormProps {
  fields: NodeUiFields[];
  onSave: (values: Record<string, any>) => void;
  onCancel: () => void;
}

const NodeForm: React.FC<NodeFormProps> = ({ fields, onSave, onCancel }) => {
  const [formValues, setFormValues] = useState<Record<string, any>>(
    fields.reduce((acc, field) => {
      acc[field.name] = field.default;
      return acc;
    }, {} as Record<string, any>)
  );

  const handleChange = (name: string, value: any) => {
    setFormValues(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const renderField = (field: NodeUiFields) => {
    switch (field.type) {
      case 'string':
        return (
          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">
              {field.label}
              {field.required && <span className="text-red-500">*</span>}
            </label>
            <input
              type="text"
              value={formValues[field.name] || ''}
              onChange={(e) => handleChange(field.name, e.target.value)}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required={field.required}
            />
            {field.description && (
              <p className="text-sm text-gray-500">{field.description}</p>
            )}
          </div>
        );
      case 'number':
        return (
          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">
              {field.label}
              {field.required && <span className="text-red-500">*</span>}
            </label>
            <input
              type="number"
              value={formValues[field.name] || ''}
              onChange={(e) => handleChange(field.name, Number(e.target.value))}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required={field.required}
            />
            {field.description && (
              <p className="text-sm text-gray-500">{field.description}</p>
            )}
          </div>
        );
      case 'boolean':
        return (
          <div className="space-y-1">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formValues[field.name] || false}
                onChange={(e) => handleChange(field.name, e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                required={field.required}
              />
              <span className="text-sm font-medium text-gray-700">
                {field.label}
                {field.required && <span className="text-red-500">*</span>}
              </span>
            </label>
            {field.description && (
              <p className="text-sm text-gray-500">{field.description}</p>
            )}
          </div>
        );
      case 'array':
        return (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              {field.label}
              {field.required && <span className="text-red-500">*</span>}
            </label>
            {(formValues[field.name] || []).map((item: any, index: number) => (
              <div key={index} className="flex space-x-2">
                <input
                  type="text"
                  value={item}
                  onChange={(e) => {
                    const newArray = [...formValues[field.name]];
                    newArray[index] = e.target.value;
                    handleChange(field.name, newArray);
                  }}
                  className="flex-1 p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <button
                  onClick={() => {
                    const newArray = formValues[field.name].filter((_: any, i: number) => i !== index);
                    handleChange(field.name, newArray);
                  }}
                  className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Remove
                </button>
              </div>
            ))}
            <button
              onClick={() => {
                handleChange(field.name, [...(formValues[field.name] || []), '']);
              }}
              className="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Add Item
            </button>
            {field.description && (
              <p className="text-sm text-gray-500">{field.description}</p>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow-lg">
      <h3 className="text-lg font-bold mb-4">Node Configuration</h3>
      <div className="space-y-4">
        {fields.map((field) => (
          <div key={field.name} className="space-y-2">
            {renderField(field)}
          </div>
        ))}
      </div>
      <div className="flex justify-end space-x-2 mt-4">
        <button
          onClick={onCancel}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
        >
          Cancel
        </button>
        <button
          onClick={() => onSave(formValues)}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Save
        </button>
      </div>
    </div>
  );
};

export default NodeForm; 