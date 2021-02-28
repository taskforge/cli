export interface Task {
  id: string; // UUID

  title: string;

  owner: string; // UUID

  source: string;
  priority: number;
  context: string;

  created_date: string | Date;
  completed_date: string | Date | null;
}

export function isTask(data: any): data is Task {
  return (
    data &&
    data.title !== undefined &&
    data.owner !== undefined &&
    data.source !== undefined &&
    data.priority !== undefined &&
    data.context !== undefined &&
    data.created_date !== undefined
  );
}
