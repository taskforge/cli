import { DEFAULT_HEADERS, Headers } from './headers';
import { Credentials } from './types';

export interface ClientOptions {
    baseUrl: string;
    headers: Headers;
    token: string;
}

export const DEFAULT_OPTIONS = {
    baseUrl: process.env.TASKFORGE_HOST
        ? process.env.TASKFORGE_HOST
        : process.env.REACT_APP_TASKFORGE_HOST
        ? process.env.REACT_APP_TASKFORGE_HOST
        : 'https://api.taskforge.io/api',
    token: process.env.TASKFORGE_TOKEN ? process.env.TASKFORGE_TOKEN : '',
    headers: DEFAULT_HEADERS
};

export function setDefaultCreds(creds: Credentials): void {
    DEFAULT_OPTIONS.token = creds.access;
}

export function url(options: ClientOptions): string {
    if (options.baseUrl && options.baseUrl !== '') {
        return options.baseUrl;
    }

    return DEFAULT_OPTIONS.baseUrl;
}
