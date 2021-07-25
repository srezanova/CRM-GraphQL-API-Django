import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useQuery, gql } from '@apollo/client';
import dayjs from 'dayjs';
import { TasksList } from '../components/TasksList/TasksList';
import type { TaskFiltersProps } from '../components/TasksList/TaskFilters/TaskFilters';

export const tasksQuery = gql`
  query tasks($customerPhone: String, $category: CategoryEnum, $createdAt: String, $dateStart: String, $dateEnd: String) {
    allTasks(customerPhone: $customerPhone, category: $category, createdAt: $createdAt, dateStart: $dateStart, dateEnd: $dateEnd) {
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

export default function Index() {
  const history = useHistory();
  const [filters, setFilters] = useState<TaskFiltersProps['values']>({
    customerPhone: '',
    category: null,
    createdAt: null,
    range: [null, null],
  });

  const handleFilterChange = (field: string, value: any) => setFilters(current => ({
    ...current,
    [field]: value,
  }));

  const { data, loading, error } = useQuery(tasksQuery, {
    variables: {
      customerPhone: filters.customerPhone.trim().length > 0 ? filters.customerPhone : undefined,
      category: filters.category || undefined,
      createdAt: filters.createdAt ? dayjs(filters.createdAt).format('YYYY-MM-DD') : undefined,
      dateStart: filters.range[0] ? dayjs(filters.range[0]).format('YYYY-MM-DD') : undefined,
      dateEnd: filters.range[1] ? dayjs(filters.range[1]).format('YYYY-MM-DD') : undefined,
    },
  });

  if (error) {
    history.push('/login');
    return null;
  }

  return (
    <div>
      <TasksList
        data={loading ? [] : data.allTasks}
        values={filters}
        onFilterChange={handleFilterChange}
      />
    </div>
  );
}
