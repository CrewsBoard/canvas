import Layout from '@/layout';
import Flow from '@/pages/flow';
import Demo from '@/pages/demo';

const PublicRoutes = {
  path: '/',
  element: <Layout />,
  children: [
    {
      path: '/',
      element: <Flow />,
    },
    {
      path: '/demo',
      element: <Demo />,
    },
  ],
};

export default PublicRoutes;
