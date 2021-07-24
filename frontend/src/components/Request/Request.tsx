import { useMutation, gql } from '@apollo/client';
import { Table, Text, Title, Container, Group, Button } from '@mantine/core';
import { Link, useHistory } from 'react-router-dom';
import dayjs from 'dayjs';
import type { Request as RequestType } from '../../types';
import { CategoryBadge } from '../RequestsList/CategoryBadge';
import { StatusBadge } from '../RequestsList/StatusBadge';
import { requestsQuery } from '../../pages/Index';

const deleteMutation = gql`
  mutation deleteRequestMutation($id: ID!) {
    deleteRequest(id: $id) {
      id
    }
  }
`;

interface RequestProps {
  data: RequestType;
}

export function Request({ data }: RequestProps) {
  const [mutate] = useMutation(deleteMutation);
  const history = useHistory();

  const handleDelete = () => {
    mutate({ variables: { id: data.id }, refetchQueries: [{ query: requestsQuery }] }).then(() => history.replace('/'));
  };

  return (
    <div style={{ marginTop: 100 }}>
      <Container>
        <div style={{ marginBottom: 30, display: 'flex', justifyContent: 'space-between' }}>
          <Title>Заявка</Title>
          <Group>
            <Button color="red" onClick={handleDelete}>Удалить заявку</Button>
            <Button component={Link} to={`/requests/${data.id}/edit`}>Редактировать</Button>
          </Group>
        </div>

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
              <td>Ответственный сотрудник</td>
              <td>{data.employee.email}</td>
            </tr>
            <tr>
              <td>Тип заявки</td>
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
