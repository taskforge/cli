export * from './task';
export * from './source';
export * from './filter';
export * from './comment';
export * from './context';
export * from './user';

export interface APIError {
    code: number;
    message?: string;
}

export function isAPIError(data: any): data is APIError {
    return data && data.code !== undefined;
}
