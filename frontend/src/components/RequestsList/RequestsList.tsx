import dayjs from 'dayjs';
import { Link } from 'react-router-dom';
import { Pencil2Icon } from '@modulz/radix-icons';
import { Paper, Table, Title, Container, Group, Button, ActionIcon, Text } from '@mantine/core';
import type { Request } from '../../types';
import { RequestFiltersProps, RequestFilters } from './RequestFilters/RequestFilters';
import { StatusBadge } from './StatusBadge';
import { CategoryBadge } from './CategoryBadge';
import useStyles from './RequestsList.styles';

interface RequestsListProps extends RequestFiltersProps {
  data: Request[];
}

export function RequestsList({ data, values, onFilterChange }: RequestsListProps) {
  const classes = useStyles();

  const rows = data.map(item => (
    <tr key={item.id}>
      <td>{item.id}</td>
      <td><Text size="xs">{item.description}</Text></td>
      <td><Text size="xs">{item.customer.phone}</Text></td>
      <td>{dayjs(item.createdAt).locale('ru').format('DD MMMM YYYY')}</td>
      <td><StatusBadge status={item.status} /></td>
      <td><CategoryBadge category={item.category} /></td>
      <td>
        <ActionIcon component={Link} to={`/requests/${item.id}/`} variant="outline">
          <Pencil2Icon />
        </ActionIcon>
      </td>
    </tr>
  ));

  return (
    <div className={classes.wrapper}>
      <Container size="xl">
        <Group position="apart" className={classes.header}>
          <Title>Все заявки</Title>
          <Button component={Link} to="/new-request/">Создать заявку</Button>
        </Group>

        <RequestFilters values={values} onFilterChange={onFilterChange} />

        <Paper shadow="sm" padding="xl">
          <Table>
            <thead>
              <tr>
                <th>Номер заявки</th>
                <th>Описание</th>
                <th>Клиент</th>
                <th>Дата создания</th>
                <th>Статус</th>
                <th>Тип заявки</th>
                <th />
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </Table>
        </Paper>
      </Container>
    </div>
  );
}
