export interface Context {
  id: string;
  name: string;
  owner: string;
}

export function isContext(data: any): data is Context {
  return data && data.id && data.name && data.owner !== undefined;
}
