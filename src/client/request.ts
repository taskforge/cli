import { headers } from './headers';
import { ClientOptions, url } from './options';

import fetch from 'node-fetch';

export interface RequestBuilder {
    endpoint: string;
    options: ClientOptions;
    token?: string;
    method?: string;
    data?: any;
    refreshToken?: string;
    params?: any;
}

export interface Request {
    endpoint: string;
    token: string;
    refreshToken: string;
    method: string;
    options: ClientOptions;
    data: any;
    params?: any;
}

export function request({
    refreshToken,
    endpoint,
    method,
    options,
    token,
    data
}: RequestBuilder): Request {
    return {
        endpoint,
        data,
        options,
        method: method ? method : 'GET',
        token: token ? token : options.token ? options.token : '',
        refreshToken: refreshToken
            ? refreshToken
            : options.refreshToken
            ? options.refreshToken
            : ''
    };
}

export async function execute(req: Request, refresh = true): Promise<any> {
    const fullUrl = `${url(req.options)}${req.endpoint}`;
    const response = await fetch(fullUrl, {
        method: req.method,
        headers: headers({
            token: req.token,
            additional: req.options.headers
        }),
        redirect: 'follow',
        body: req.data ? JSON.stringify(req.data) : undefined
    });

    if (response.status === 401 && refresh && req.endpoint != 'api/token') {
        const { access } = await execute(
            {
                ...req,
                endpoint: '/token/refresh',
                method: 'POST',
                data: { access: req.token, refresh: req.refreshToken },
                token: req.token
            },
            false
        );

        req.token = access;
        return execute(req, false);
    }

    if (response.status === 500) {
        throw new Error(`Unexpected error: ${await response.text()}`);
    }

    return {
        code: response.status,
        data: await response.json()
    };
}
