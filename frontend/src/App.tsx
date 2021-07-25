import { BrowserRouter, Route } from 'react-router-dom';
import { Provider } from './components/Provider/Provider';
import Login from './pages/Login';
import Index from './pages/Index';
import Task from './pages/Task';
import NewTask from './pages/NewTask';
import EditTask from './pages/EditTask';

export function App() {
  return (
    <Provider>
      <BrowserRouter>
        <Route path="/" exact>
          <Index />
        </Route>

        <Route path="/new-task" exact>
          <NewTask />
        </Route>

        <Route path="/tasks/:id/" exact>
          <Task />
        </Route>

        <Route path="/tasks/:id/edit" exact>
          <EditTask />
        </Route>

        <Route path="/login">
          <Login />
        </Route>
      </BrowserRouter>
    </Provider>
  );
}
