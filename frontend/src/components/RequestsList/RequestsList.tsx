import dayjs from 'dayjs';
import { Link } from 'react-router-dom';
import { Pencil2Icon } from '@modulz/radix-icons';
import { Paper, Table, Title, Container, Group, Button, ActionIcon, Text } from '@mantine/core';
import { StatusBadge } from './StatusBadge';
import { CategoryBadge } from './CategoryBadge';
import type { Request } from '../../types';
import useStyles from './RequestsList.styles';

interface RequestsListProps {
  data: Request[];
}

export function RequestsList({ data }: RequestsListProps) {
  const classes = useStyles();

  const rows = data.map(item => (
    <tr key={item.id}>
      <td>{item.id}</td>
      <td><Text size="xs">{item.description}</Text></td>
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
      <Container>
        <Group position="apart" className={classes.header}>
          <Title>Все заявки</Title>
          <Button component={Link} to="/requests/new/">Создать заявку</Button>
        </Group>

        <Paper shadow="sm" padding="xl">
          <Table>
            <thead>
              <tr>
                <th>Номер заявки</th>
                <th>Описание</th>
                <th>Дата создания</th>
                <th>Статус</th>
                <th>Категория</th>
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
