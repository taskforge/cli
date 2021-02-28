import { Column } from './filter';

export interface Settings {
  user: string;
  default_columns: Column[];
  default_context: string | null;
}

export function isSettings(data: any): data is Settings {
  return (
    data !== undefined &&
    data.user !== undefined &&
    data.default_columns !== undefined &&
    Array.isArray(data.default_columns) &&
    data.default_context !== undefined
  );
}
