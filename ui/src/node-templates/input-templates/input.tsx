import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

const formSchema = z.object({
  inputData: z.string().min(1, 'Input Data is required'),
});

type FormValues = z.infer<typeof formSchema>;

export default function CrewAiAgentTemplate() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      inputData: '',
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
