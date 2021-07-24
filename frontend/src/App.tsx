import { BrowserRouter, Route } from 'react-router-dom';
import { Provider } from './components/Provider/Provider';
import Login from './pages/Login';
import Index from './pages/Index';
import Request from './pages/Request';
import NewRequest from './pages/NewRequest';
import EditRequest from './pages/EditRequest';

export function App() {
  return (
    <Provider>
      <BrowserRouter>
        <Route path="/" exact>
          <Index />
        </Route>

        <Route path="/new-request" exact>
          <NewRequest />
        </Route>

        <Route path="/requests/:id/" exact>
          <Request />
        </Route>

        <Route path="/requests/:id/edit" exact>
          <EditRequest />
        </Route>

        <Route path="/login">
          <Login />
        </Route>
      </BrowserRouter>
    </Provider>
  );
}
