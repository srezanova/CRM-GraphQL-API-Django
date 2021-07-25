import { useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { useMutation, gql } from '@apollo/client';
import { TaskForm, TaskFormValues } from '../components/TaskForm/TaskForm';

const createNewTask = gql`
  mutation createNewTask($input: TaskInput!) {
    createTask(taskData: $input) {
      task {
        id
      }
    }
  }
`;

export default function NewTask() {
  const history = useHistory();
  const [mutate] = useMutation(createNewTask);

  useEffect(() => {
    if (!localStorage.getItem('auth')) {
      history.push('/login');
    }
  }, []);

  const handleSubmit = (values: TaskFormValues) => {
    mutate({ variables: { input: values } }).then(response => history.push(`/tasks/${response.data.createTask.task.id}`));
  };

  return <TaskForm title="Создать новую заявку" onSubmit={handleSubmit} />;
}
