export interface Source {
  id: string;
  name: string;
}

export function isSource(data: any): data is Source {
  return data !== undefined && data.id !== undefined && data.name !== undefined;
}
