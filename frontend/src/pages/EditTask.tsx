import { useHistory, useParams } from 'react-router-dom';
import { useMutation, useQuery, gql } from '@apollo/client';
import { LoadingOverlay } from '@mantine/core';
import { TaskForm, TaskFormValues } from '../components/TaskForm/TaskForm';
import { taskQuery } from './Task';

const updateTask = gql`
  mutation updateTask($input: TaskInput!) {
    updateTask(taskData: $input) {
      task {
        id
      }
    }
  }
`;

export default function EditTask() {
  const params = useParams<{ id: string }>();
  const history = useHistory();
  const { data, loading, error } = useQuery(taskQuery, { variables: { id: params.id } });

  const [mutate] = useMutation(updateTask);
  const handleSubmit = (values: TaskFormValues) => {
    const input = {
      id: params.id,
      description: values.description,
      customerPhone: values.customerPhone,
      category: values.category,
      status: values.status,
    };

    mutate({ variables: { input }, refetchQueries: [{ query: taskQuery, variables: { id: params.id } }] }).then(response => history.push(`/tasks/${response.data.updateTask.task.id}`));
  };

  if (loading) {
    return <LoadingOverlay visible />;
  }

  if (error) {
    history.push('/login');
    return null;
  }

  return <TaskForm title="Редактировать заявку" onSubmit={handleSubmit} initialValues={{ ...data.taskById, customerPhone: data.taskById.customer.phone }} />;
}
