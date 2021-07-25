import { Badge } from '@mantine/core';
import type { Status } from '../../types';

interface StatusBadgeProps {
  status: Status;
}

export const data: Record<Status, { color: string; name: string }> = {
  ACCEPTED: {
    name: 'Принято',
    color: 'teal',
  },

  IN_PROGRESS: {
    name: 'В работе',
    color: 'indigo',
  },

  READY: {
    name: 'Готово',
    color: 'red',
  },

  CLOSED: {
    name: 'Закрыто',
    color: 'gray',
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const { name, color } = data[status];
  return <Badge color={color} variant="outline">{name}</Badge>;
}
