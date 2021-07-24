export type Category = 'CONSULTING' | 'DIAGNOSIS' | 'REPAIR' | 'OTHER';
export type Status = 'ACCEPTED' | 'IN_PROGRESS' | 'READY' | 'CLOSED';

export interface Request {
  id: string;
  createdAt: string;
  employee: { id: string; email: string };
  category: Category | null;
  status: Status | null;
  description: string;
  customer: { id: string; phone: string; name: string };
}
