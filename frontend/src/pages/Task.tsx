import { useQuery, gql } from '@apollo/client';
import { LoadingOverlay } from '@mantine/core';
import { useParams, useHistory } from 'react-router-dom';
import { Task } from '../components/Task/Task';

export const taskQuery = gql`
  query taskQuery($id: ID!) {
    taskById(id: $id) {
      id
      createdAt
      employee {
        id
        email
      }
      category
      status
      description
      customer {
        id
        name
        phone
      }
    }
  }
`;

export default function TaskPage() {
  const history = useHistory();
  const params = useParams<{ id: string }>();
  const { data, loading, error } = useQuery(taskQuery, { variables: { id: params.id } });

  if (error) {
    history.push('/login');
    return null;
  }

  return (
    <div>
      {loading ? <LoadingOverlay visible /> : <Task data={data.taskById} />}
    </div>
  );
}
