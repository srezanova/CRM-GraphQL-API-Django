import { Badge } from '@mantine/core';

export type Category = 'CONSULTING' | 'DIAGNOSIS' | 'REPAIR' | 'REPLACEMENT' | 'RETURN' | 'COMPLAINT' | 'OTHER';

interface CategoryBadgeProps {
  category: Category;
}

const data: Record<Category, { color: string; name: string }> = {
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

  REPLACEMENT: {
    name: 'Замена',
    color: 'red',
  },

  RETURN: {
    name: 'Возврат',
    color: 'violet',
  },

  COMPLAINT: {
    name: 'Жалоба',
    color: 'cyan',
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
