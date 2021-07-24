import { useQuery, gql } from '@apollo/client';
import { LoadingOverlay } from '@mantine/core';
import { useParams } from 'react-router-dom';
import { Request } from '../components/Request/Request';

export const requestQuery = gql`
  query requestQuery($id: ID!) {
    requestById(id: $id) {
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

export default function RequestPage() {
  const params = useParams<{ id: string }>();
  const { data, loading } = useQuery(requestQuery, { variables: { id: params.id } });
  return (
    <div>
      {loading ? <LoadingOverlay visible /> : <Request data={data.requestById} />}
    </div>
  );
}
