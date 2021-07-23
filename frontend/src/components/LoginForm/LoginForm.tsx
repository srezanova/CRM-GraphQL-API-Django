import { TextInput, PasswordInput, Paper, Button, LoadingOverlay, Text } from '@mantine/core';
import { useForm } from '@mantine/hooks';

export interface LoginValues {
  email: string;
  password: string;
}

interface LoginFormProps {
  onSubmit(values: LoginValues): void;
  loading: boolean;
  error: string | boolean;
}

export function LoginForm({ onSubmit, loading, error }: LoginFormProps) {
  const form = useForm({
    initialValues: { email: '', password: '' },
    validationRules: {
      email: (val) => val.includes('@'),
      password: (val) => val.trim().length > 0,
    },
  });

  const handleSubmit = (_values: any) => {
    onSubmit(_values);
  };

  return (
    <Paper style={{ position: 'relative' }}>
      <LoadingOverlay visible={loading} />
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <TextInput
          label="Почта"
          placeholder="email@example.com"
          value={form.values.email}
          onChange={(event) => form.setFieldValue('email', event.currentTarget.value)}
          error={form.errors.email && 'Введите корректный email'}
        />

        <PasswordInput
          label="Пароль"
          placeholder="Пароль"
          value={form.values.password}
          onChange={(event) => form.setFieldValue('password', event.currentTarget.value)}
          error={form.errors.password && 'Введите корректный пароль'}
        />

        {error && <Text color="red" size="sm">{error}</Text>}

        <Button type="submit">Войти</Button>
      </form>
    </Paper>
  );
}
