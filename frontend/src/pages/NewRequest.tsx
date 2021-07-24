import { useHistory } from 'react-router-dom';
import { useMutation, gql } from '@apollo/client';
import { RequestForm, RequestFormValues } from '../components/RequestForm/RequestForm';

const createNewRequest = gql`
  mutation createNewRequest($input: RequestInput!) {
    createRequest(requestData: $input) {
      request {
        id
      }
    }
  }
`;

export default function NewRequest() {
  const history = useHistory();
  const [mutate] = useMutation(createNewRequest);
  const handleSubmit = (values: RequestFormValues) => {
    mutate({ variables: { input: values } }).then(response => history.push(`/requests/${response.data.createRequest.request.id}`));
  };

  return <RequestForm title="Создать новую заявку" onSubmit={handleSubmit} />;
}
