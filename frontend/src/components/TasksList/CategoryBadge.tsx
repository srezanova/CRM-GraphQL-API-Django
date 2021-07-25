import { Badge } from '@mantine/core';
import type { Category } from '../../types';

interface CategoryBadgeProps {
  category: Category;
}

export const data: Record<Category, { color: string; name: string }> = {
  CONSULTING: {
    name: 'Консультация',
    color: 'grape',
  },

  DIAGNOSIS: {
    name: 'Диагностика',
    color: 'indigo',
  },

  REPAIR: {
    name: 'Ремонт',
    color: 'blue',
  },

  OTHER: {
    name: 'Прочее',
    color: 'gray',
  },
};

export function CategoryBadge({ category }: CategoryBadgeProps) {
  const { name, color } = data[category];
  return <Badge color={color} variant="light">{name}</Badge>;
}
