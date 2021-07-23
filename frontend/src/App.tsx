import { BrowserRouter, Route } from 'react-router-dom';
import { Provider } from './components/Provider/Provider';
import Login from './pages/Login';
import Request from './pages/Request';

export function App() {
  return (
    <Provider>
      <BrowserRouter>
        <Route path="/" exact>
          <Request />
        </Route>

        <Route path="/login">
          <Login />
        </Route>
      </BrowserRouter>
    </Provider>
  );
}
