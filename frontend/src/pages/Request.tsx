import { LoadingOverlay } from '@mantine/core';
import { useQuery, gql } from '@apollo/client';
import { RequestsList } from '../components/RequestsList/RequestsList';

const requestsQuery = gql`
  query requests {
    allRequests {
      id
      createdAt
      category
      status
      description
      customer {
        id
        phone
        name
      }
      employee {
        id
        email
      }
    }
  }
`;

export default function Request() {
  const { data, loading } = useQuery(requestsQuery);

  if (loading) {
    return <LoadingOverlay visible />;
  }

  return (
    <div>
      <RequestsList data={data.allRequests} />
    </div>
  );
}
