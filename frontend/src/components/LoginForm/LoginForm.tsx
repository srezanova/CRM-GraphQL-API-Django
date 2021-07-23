import { TextInput, PasswordInput, Paper, Button, LoadingOverlay, Text, Title, Group } from '@mantine/core';
import { useForm } from '@mantine/hooks';
import useStyles from './LoginForm.styles';

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
  const classes = useStyles();
  const form = useForm({
    initialValues: { email: '', password: '' },
    validationRules: {
      email: (val) => val.includes('@'),
      password: (val) => val.trim().length > 0,
    },
  });

  const onFill = () => {
    form.setValues({ email: 'employee@email.com', password: 'testpassword' });
  };

  const handleSubmit = (_values: any) => {
    onSubmit(_values);
  };

  return (
    <div className={classes.wrapper}>
      <Paper className={classes.inner} shadow="sm" padding="xl">
        <LoadingOverlay visible={loading} />

        <Title align="center" className={classes.title}>Войти</Title>

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            className={classes.field}
            label="Почта"
            placeholder="email@example.com"
            value={form.values.email}
            onChange={(event) => form.setFieldValue('email', event.currentTarget.value)}
            error={form.errors.email && 'Введите корректный email'}
          />

          <PasswordInput
            className={classes.field}
            label="Пароль"
            placeholder="Пароль"
            value={form.values.password}
            onChange={(event) => form.setFieldValue('password', event.currentTarget.value)}
            error={form.errors.password && 'Введите корректный пароль'}
          />

          {error && <Text color="red" size="sm">{error}</Text>}

          <Group position="apart" className={classes.controls}>
            <Button color="gray" variant="link" onClick={onFill}>Демо пользователь (сотрудник)</Button>
            <Button type="submit">Войти</Button>
          </Group>
        </form>
      </Paper>
    </div>
  );
}
