import { useHistory, useParams } from 'react-router-dom';
import { useMutation, useQuery, gql } from '@apollo/client';
import { LoadingOverlay } from '@mantine/core';
import { RequestForm, RequestFormValues } from '../components/RequestForm/RequestForm';
import { requestQuery } from './Request';

const updateRequest = gql`
  mutation updateRequest($input: RequestInput!) {
    updateRequest(requestData: $input) {
      request {
        id
      }
    }
  }
`;

export default function EditRequest() {
  const params = useParams<{ id: string }>();
  const history = useHistory();
  const { data, loading } = useQuery(requestQuery, { variables: { id: params.id } });

  const [mutate] = useMutation(updateRequest);
  const handleSubmit = (values: RequestFormValues) => {
    const input = {
      id: params.id,
      description: values.description,
      customerPhone: values.customerPhone,
      category: values.category,
      status: values.status,
    };

    mutate({ variables: { input }, refetchQueries: [{ query: requestQuery, variables: { id: params.id } }] }).then(response => history.push(`/requests/${response.data.updateRequest.request.id}`));
  };

  if (loading) {
    return <LoadingOverlay visible />;
  }

  return <RequestForm title="Редактировать заявку" onSubmit={handleSubmit} initialValues={{ ...data.requestById, customerPhone: data.requestById.customer.phone }} />;
}
