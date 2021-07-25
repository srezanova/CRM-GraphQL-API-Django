import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useMutation, gql } from '@apollo/client';
import { LoginForm, LoginValues } from '../components/LoginForm/LoginForm';

const mutation = gql`
  mutation login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      token
      errors
    }
  }
`;

export default function Login() {
  const history = useHistory();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [mutate] = useMutation(mutation);

  const handleSubmit = (values: LoginValues) => {
    setLoading(true);
    mutate({ variables: values }).then(response => {
      const token = response.data.login.token as string;
      if (!token) {
        setError(true);
      } else {
        setError(false);
        window.localStorage.setItem('auth', token);
        history.push('/');
      }

      setLoading(false);
    });
  };

  return (
    <LoginForm onSubmit={handleSubmit} loading={loading} error={error && 'Неверная почта или пароль'} />
  );
}
