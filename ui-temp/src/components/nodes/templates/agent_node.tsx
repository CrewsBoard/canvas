// components/AgentForm.tsx
import React from 'react';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { InfoNodeData } from '../types/info-node';

type AgentTemplateProps = {
  data: InfoNodeData;
};

// Zod schema
const formSchema = z.object({
  agent_role: z.string().min(1, 'Agent Role is required'),
  agent_goal: z.string().min(1, 'Agent Goal is required'),
});

type FormSchema = z.infer<typeof formSchema>;

const AgentTemplate: React.FC<AgentTemplateProps> = ({ data }) => {
  const form = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      agent_role: '',
      agent_goal: '',
    },
  });

  const onSubmit = (values: FormSchema) => {
    console.log('Form submitted:', values);
  };

  // Validate and extract title and description
  const title =
    data.data && typeof data.data.title === 'string' ? data.data.title : '';
  const description =
    data.data && typeof data.data.description === 'string'
      ? data.data.description
      : '';

  return (
    <Card className="w-[350px]">
      <CardHeader className="cursor-grab">
        {title && <CardTitle>{title}</CardTitle>}
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent className="nodrag">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            {/* Agent Role */}
            <FormField
              control={form.control}
              name="agent_role"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Agent Role</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter the agent's role" {...field} />
                  </FormControl>
                  <FormDescription>
                    This is the role of the agent.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Agent Goal */}
            <FormField
              control={form.control}
              name="agent_goal"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Agent Goal</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter the agent's goal" {...field} />
                  </FormControl>
                  <FormDescription>
                    This is the goal assigned to the agent.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type="submit">Submit</Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter className="flex justify-between nodrag">
        <Button variant="outline">Cancel</Button>
        <Button>Deploy</Button>
      </CardFooter>
    </Card>
  );
};

export default AgentTemplate;
