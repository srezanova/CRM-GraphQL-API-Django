import { BrowserRouter, Route } from 'react-router-dom';
import { Provider } from './components/Provider/Provider';
import Login from './pages/Login';
import Request from './pages/Request';
import NewRequest from './pages/NewRequest';

export function App() {
  return (
    <Provider>
      <BrowserRouter>
        <Route path="/" exact>
          <Request />
        </Route>

        <Route path="/requests/new/" exact>
          <NewRequest />
        </Route>

        <Route path="/login">
          <Login />
        </Route>
      </BrowserRouter>
    </Provider>
  );
}
