import { Title, TextInput, Select } from '@mantine/core';
import { useForm } from '@mantine/hooks';
import type { Category, Status } from '../../types';
import { data as STATUS_DATA } from '../RequestsList/StatusBadge';
import { data as CATEGORY_DATA } from '../RequestsList/CategoryBadge';
import useStyles from './RequestForm.styles';

interface RequestFormValues {
  product: string;
  problem: string;
  solution: string;
  category: Category | null;
  status: Status | null;
  contacts: string;
  clientId: string;
}

interface RequestFormProps {
  title: string;
  initialValues?: RequestFormValues;
}

const DEFAULT_VALUES = {
  product: '',
  problem: '',
  solution: '',
  category: null,
  status: null,
  contacts: '',
  clientId: '',
};

const statuses = Object.keys(STATUS_DATA).map(key => ({
  value: key,
  label: STATUS_DATA[key].name,
}));

const categories = Object.keys(CATEGORY_DATA).map(key => ({
  value: key,
  label: CATEGORY_DATA[key].name,
}));

export function RequestForm({ title, initialValues }: RequestFormProps) {
  const classes = useStyles();
  const form = useForm({
    initialValues: initialValues || DEFAULT_VALUES,
    validationRules: {},
  });

  return (
    <div className={classes.wrapper}>
      <Title>{title}</Title>

      <TextInput
        label="Телефон клиента"
        placeholder="Телефон клиента"
        value={form.values.clientId}
        onChange={event => form.setFieldValue('clientId', event.currentTarget.value)}
        error={form.errors.clientId && 'Введите значение'}
      />

      <TextInput
        label="Устройство"
        placeholder="Устройство"
        value={form.values.product}
        onChange={event => form.setFieldValue('product', event.currentTarget.value)}
        error={form.errors.product && 'Введите значение'}
      />

      <TextInput
        label="Неисправность"
        placeholder="Неисправность"
        value={form.values.problem}
        onChange={event => form.setFieldValue('problem', event.currentTarget.value)}
        error={form.errors.problem && 'Введите значение'}
      />

      <Select
        data={statuses}
        label="Статус"
        placeholder="Статус"
        value={form.values.status as string}
        onChange={value => form.setFieldValue('status', value as Status)}
        error={form.errors.status && 'Введите значение'}
      />

      <Select
        data={categories}
        label="Статус"
        placeholder="Статус"
        value={form.values.status as string}
        onChange={value => form.setFieldValue('status', value as Status)}
        error={form.errors.status && 'Введите значение'}
      />
    </div>
  );
}
