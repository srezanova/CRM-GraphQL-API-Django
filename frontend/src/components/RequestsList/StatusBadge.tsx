import { Badge } from '@mantine/core';

export type Status = 'OPEN' | 'SCHEDULED' | 'CANCELED' | 'CLOSED';

interface StatusBadgeProps {
  status: Status;
}

const data: Record<Status, { color: string; name: string }> = {
  OPEN: {
    name: 'Открыта',
    color: 'teal',
  },

  SCHEDULED: {
    name: 'Запланирована',
    color: 'indigo',
  },

  CANCELED: {
    name: 'Отменена',
    color: 'red',
  },

  CLOSED: {
    name: 'Закрыта',
    color: 'gray',
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const { name, color } = data[status];
  return <Badge color={color} variant="outline">{name}</Badge>;
}
