import { zodResolver } from '@hookform/resolvers/zod';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useFlowStateStore } from '@/stores/flowStateStore';

const formSchema = z.object({
    inputData: z.string().min(1, 'Input Data is required'),
    inputLabel: z.string().optional(),
    description: z.string().optional(),
});

type FormValues = z.infer<typeof formSchema>;

export default function InputTemplate() {
    const { selectedNode, setSelectedNode, setNodeById } = useFlowStateStore();

    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            inputData: (selectedNode?.data?.inputData as string) || '',
            inputLabel: (selectedNode?.data?.inputLabel as string) || '',
            description: (selectedNode?.data?.description as string) || '',
        },
    });

    useEffect(() => {
        if (selectedNode) {
            const subscription = form.watch(values => {
                const updatedNode = {
                    ...selectedNode,
                    data: {
                        ...selectedNode.data,
                        ...values,
                    },
                };
                setNodeById(selectedNode.id, updatedNode);
                setSelectedNode(updatedNode);
            });
            return () => subscription.unsubscribe();
        }
    }, [form, selectedNode, setNodeById, setSelectedNode]);

    return (
        <Form {...form}>
            <form className="space-y-4">
                <FormField
                    control={form.control}
                    name="inputLabel"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Input Label</FormLabel>
                            <FormControl>
                                <Input placeholder="Enter input label" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="description"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Description</FormLabel>
                            <FormControl>
                                <Input placeholder="Enter description" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="inputData"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Input Data</FormLabel>
                            <FormControl>
                                <Input placeholder="Enter input data" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            </form>
        </Form>
    );
}
