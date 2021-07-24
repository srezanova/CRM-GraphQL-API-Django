import { Table, Text, Title, Container, Group, Button } from '@mantine/core';
import { Link } from 'react-router-dom';
import dayjs from 'dayjs';
import type { Request as RequestType } from '../../types';
import { CategoryBadge } from '../RequestsList/CategoryBadge';
import { StatusBadge } from '../RequestsList/StatusBadge';

interface RequestProps {
  data: RequestType;
}

export function Request({ data }: RequestProps) {
  return (
    <div style={{ marginTop: 100 }}>
      <Container>
        <Group position="apart" style={{ marginBottom: 30 }}>
          <Title>Заявка</Title>
          <Button component={Link} to={`/requests/${data.id}/edit`}>Редактировать</Button>
        </Group>

        <Table>
          <tbody>
            <tr>
              <td>Номер заявки</td>
              <td>{data.id}</td>
            </tr>
            <tr>
              <td>Дата создания</td>
              <td>{dayjs(data.createdAt).locale('ru').format('DD MMMM YYYY')}</td>
            </tr>
            <tr>
              <td>Телефон клиента</td>
              <td>{data.customer.phone}</td>
            </tr>
            <tr>
              <td>Имя клиента</td>
              <td>{data.customer.name}</td>
            </tr>
            <tr>
              <td>Ответсвтенный сотрудник</td>
              <td>{data.employee.email}</td>
            </tr>
            <tr>
              <td>Категория</td>
              <td><CategoryBadge category={data.category} /></td>
            </tr>
            <tr>
              <td>Статус</td>
              <td><StatusBadge status={data.status} /></td>
            </tr>
            <tr>
              <td>Описание</td>
              <td><Text size="sm">{data.description}</Text></td>
            </tr>
          </tbody>
        </Table>
      </Container>
    </div>
  );
}
