import { BrowserRouter, Route } from 'react-router-dom';
import { Provider } from './components/Provider/Provider';
import Login from './pages/Login';
import Index from './pages/Index';
import Request from './pages/Request';
import NewRequest from './pages/NewRequest';

export function App() {
  return (
    <Provider>
      <BrowserRouter>
        <Route path="/" exact>
          <Index />
        </Route>

        <Route path="/requests/new/" exact>
          <NewRequest />
        </Route>

        <Route path="/requests/:id/" exact>
          <Request />
        </Route>

        <Route path="/login">
          <Login />
        </Route>
      </BrowserRouter>
    </Provider>
  );
}
