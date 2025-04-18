import { Button } from '@/components/ui/button';

interface ContainerProps {
  children: React.ReactNode;
}

export default function Container({ children }: ContainerProps) {
  return (
    <div className="flex flex-col w-[400px] h-[89vh] bg-white rounded-2xl shadow border-2">
      <div className="flex justify-between rounded-t-2xl mb-4 p-4 bg-gray-50">
        <div>
          <h4 className="text-lg font-semibold">Node</h4>
          <p>
            More about nodes{' '}
            <a className="underline text-blue-500" href="#">
              Learn More
            </a>
          </p>
        </div>
        <Button>Save & Close</Button>
      </div>
      <div className="flex-grow h-full overflow-y-scroll hide-scrollbar">
        {children}
      </div>
    </div>
  );
}
