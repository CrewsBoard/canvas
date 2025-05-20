import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Checkbox } from '@/components/ui/checkbox';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

const formSchema = z.object({
    agentRole: z.string().min(1, 'Agent Role is required'),
    agentGoal: z.string().min(1, 'Agent Goal is required'),
    agentBackstory: z.string().min(1, 'Agent Backstory is required'),
    agentTools: z.string().array().optional(),
    maxIterations: z.number().optional(),
    allowDelegation: z.boolean().optional(),
    modelId: z.string().array().min(1, 'Model ID is required'),
});

type FormValues = z.infer<typeof formSchema>;

export default function CrewAiAgentTemplate() {
    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            agentRole: '',
            agentGoal: '',
            agentBackstory: '',
            agentTools: [],
            maxIterations: 1,
            allowDelegation: false,
            modelId: ['default-model'],
        },
    });

    function onSubmit(values: FormValues) {
        console.log('Submitted Values:', values);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                    control={form.control}
                    name="agentRole"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Agent Role</FormLabel>
                            <FormControl>
                                <Input placeholder="Enter agent role" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="agentGoal"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Agent Goal</FormLabel>
                            <FormControl>
                                <Input placeholder="Enter agent goal" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="agentBackstory"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Agent Backstory</FormLabel>
                            <FormControl>
                                <Textarea placeholder="Enter agent backstory" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="agentTools"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Agent Tools</FormLabel>
                            <FormControl>
                                <Input placeholder="Comma-separated tools (e.g., tool1, tool2)" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="maxIterations"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Max Iterations</FormLabel>
                            <FormControl>
                                <Input type="number" placeholder="Max Iterations" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="allowDelegation"
                    render={({ field }) => (
                        <FormItem className="flex items-center space-x-2">
                            <FormControl>
                                <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                            </FormControl>
                            <div>
                                <FormLabel>Allow Delegation</FormLabel>
                                <FormDescription>Enable if agent can delegate</FormDescription>
                            </div>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="modelId"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Model ID</FormLabel>
                            <FormControl>
                                <Input placeholder="Comma-separated model IDs" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            </form>
        </Form>
    );
}
