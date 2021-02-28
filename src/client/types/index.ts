export * from './task';
export * from './source';
export * from './filter';
export * from './comment';
export * from './context';
export * from './user';
export * from './settings';
export * from './paginated';

export interface APIError {
  message?: string;
  detail?: string;
}

export function isAPIError(data: any): data is APIError {
  return data && (data.detail !== undefined || data.message !== undefined);
}
