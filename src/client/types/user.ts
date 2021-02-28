export interface User {
  id: string;
  email: string;
  avatar_url: string;

  full_name?: string;
}

export function isUser(data: any): data is User {
  return (
    data !== undefined &&
    data.id !== undefined &&
    data.email !== undefined &&
    data.avatar_url !== undefined
  );
}

export interface Credentials {
  access: string;
  refresh: string | undefined;
}

export function isCredentials(data: any): data is Credentials {
  return data && data.access;
}

export interface PAT {
  pat: string;
}

export function isPAT(data: any): data is PAT {
  return data && data.pat;
}
