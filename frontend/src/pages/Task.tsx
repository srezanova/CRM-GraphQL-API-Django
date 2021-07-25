import { useQuery, gql } from '@apollo/client';
import { LoadingOverlay } from '@mantine/core';
import { useParams } from 'react-router-dom';
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
  const params = useParams<{ id: string }>();
  const { data, loading } = useQuery(taskQuery, { variables: { id: params.id } });
  return (
    <div>
      {loading ? <LoadingOverlay visible /> : <Task data={data.taskById} />}
    </div>
  );
}
