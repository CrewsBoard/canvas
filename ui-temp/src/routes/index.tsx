import { useRoutes } from 'react-router-dom';

import PublicRoutes from './public';

export default function Routes() {
  return useRoutes([PublicRoutes]);
}
