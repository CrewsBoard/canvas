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

type OutputTemplateProps = {
  data: InfoNodeData;
};

// Zod schema
const formSchema = z.object({
  output_data: z.string().min(1, 'Output data is required'),
});

type FormSchema = z.infer<typeof formSchema>;

const OutpuTemplate: React.FC<OutputTemplateProps> = ({ data }) => {
  const form = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      output_data: '',
    },
  });

  const onSubmit = (values: FormSchema) => {
    console.log('Form submitted:', values);
  };

  // Validate and extract title and description
  const title = data && typeof data.title === 'string' ? data.title : '';
  const description =
    data && typeof data.description === 'string' ? data.description : '';

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
              name="output_data"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Output Data</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter the agent's role" {...field} />
                  </FormControl>
                  <FormDescription>Output data for the flow</FormDescription>
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

export default OutpuTemplate;
