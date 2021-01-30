export type Headers = { [name: string]: string };

export const DEFAULT_HEADERS: Headers = {
    'Content-Type': 'application/json',
    Accepts: 'application/json'
};

export interface HeaderOptions {
    token?: string;
    additional?: Headers;
}

export function headers({ token, additional }: HeaderOptions): Headers {
    const extraHeaders = additional ? additional : {};
    if (token && token !== '') {
        extraHeaders['Authorization'] = `Bearer ${token}`;
    }

    return {
        ...DEFAULT_HEADERS,
        ...extraHeaders
    };
}
