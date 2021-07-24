import { Select, TextInput } from '@mantine/core';
import { DateRangePicker, DatePicker } from '@mantine/dates';
import { data as CATEGORY_DATA } from '../CategoryBadge';
import type { Category } from '../../../types';
import useStyles from './RequestFilters.styles';

export interface RequestFiltersProps {
  values: {
    customerPhone: string;
    category: Category;
    createdAt: Date;
    range: [Date, Date];
  };

  onFilterChange(field: string, value: any): void;
}

const categories = Object.keys(CATEGORY_DATA).map(key => ({
  value: key,
  label: CATEGORY_DATA[key].name,
}));

export function RequestFilters({ values, onFilterChange }: RequestFiltersProps) {
  const classes = useStyles();

  return (
    <div className={classes.wrapper}>
      <TextInput
        className={classes.field}
        label="Телефон клиента"
        placeholder="Телефон клиента"
        value={values.customerPhone}
        onChange={(event) => onFilterChange('customerPhone', event.currentTarget.value)}
      />
      <Select
        className={classes.field}
        data={categories}
        label="Тип заявки"
        placeholder="Тип заявки"
        value={values.category}
        onChange={(value) => onFilterChange('category', value)}
        clearable
      />
      <DatePicker
        className={classes.field}
        locale="ru"
        label="Дата создания"
        placeholder="Дата создания"
        value={values.createdAt}
        onChange={(value) => onFilterChange('createdAt', value)}
      />
      <DateRangePicker
        className={classes.field}
        locale="ru"
        inputFormat="DD MMMM"
        label="Интервал"
        placeholder="Интервал"
        value={values.range}
        onChange={(value) => onFilterChange('range', value)}
      />
    </div>
  );
}
