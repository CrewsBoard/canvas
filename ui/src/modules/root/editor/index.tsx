import Container from '@/modules/root/editor/container';
import NodeTemplateFactory from '@/node-templates/NodeTemplateFactory';

type NodeEditorProps = {
    templateType: string;
};

export default function NodeEditor({ templateType }: NodeEditorProps) {
    return (
        <Container>
            <div className="px-4">
                <NodeTemplateFactory type={templateType} />
            </div>
        </Container>
    );
}
