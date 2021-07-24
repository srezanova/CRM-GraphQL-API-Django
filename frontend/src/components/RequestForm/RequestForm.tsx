import { Title, TextInput, Select, Textarea, Button, Paper, Group } from '@mantine/core';
import { useForm } from '@mantine/hooks';
import type { Status, Category } from '../../types';
import { data as STATUS_DATA } from '../RequestsList/StatusBadge';
import { data as CATEGORY_DATA } from '../RequestsList/CategoryBadge';
import useStyles from './RequestForm.styles';

export interface RequestFormValues {
  category: Category;
  status: Status;
  description: string;
  customerPhone: string;
}

interface RequestFormProps {
  title: string;
  initialValues?: RequestFormValues;
  onSubmit(values: RequestFormValues): void;
}

const DEFAULT_VALUES: RequestFormValues = {
  category: null,
  status: 'ACCEPTED',
  description: '',
  customerPhone: '',
};

const statuses = Object.keys(STATUS_DATA).map(key => ({
  value: key,
  label: STATUS_DATA[key].name,
}));

const categories = Object.keys(CATEGORY_DATA).map(key => ({
  value: key,
  label: CATEGORY_DATA[key].name,
}));

const nonEmpty = (val: string) => val && val.trim().length > 0;

export function RequestForm({ title, initialValues, onSubmit }: RequestFormProps) {
  const classes = useStyles();
  const form = useForm<RequestFormValues>({
    initialValues: initialValues || DEFAULT_VALUES,
    validationRules: {
      category: nonEmpty,
      status: nonEmpty,
      description: nonEmpty,
      customerPhone: nonEmpty,
    },
  });

  return (
    <div className={classes.wrapper}>
      <Paper shadow="sm" padding="xl" className={classes.inner}>
        <Title align="center" className={classes.title}>{title}</Title>

        <form onSubmit={form.onSubmit(onSubmit)}>
          <TextInput
            className={classes.field}
            label="Телефон клиента"
            placeholder="Телефон клиента"
            value={form.values.customerPhone}
            onChange={event => form.setFieldValue('customerPhone', event.currentTarget.value)}
            error={form.errors.customerPhone && 'Введите значение'}
          />

          <Textarea
            className={classes.field}
            label="Описание"
            placeholder="Описание"
            autosize
            value={form.values.description}
            onChange={event => form.setFieldValue('description', event.currentTarget.value)}
            error={form.errors.description && 'Введите значение'}
          />

          <Select
            className={classes.field}
            data={statuses}
            label="Статус"
            placeholder="Статус"
            value={form.values.status as string}
            onChange={value => form.setFieldValue('status', value as Status)}
            error={form.errors.status && 'Введите значение'}
          />

          <Select
            className={classes.field}
            data={categories}
            label="Категория"
            placeholder="Категория"
            value={form.values.category as string}
            onChange={value => form.setFieldValue('category', value as Category)}
            error={form.errors.category && 'Введите значение'}
          />

          <Group position="right">
            <Button type="submit">Создать заявку</Button>
          </Group>
        </form>
      </Paper>
    </div>
  );
}
