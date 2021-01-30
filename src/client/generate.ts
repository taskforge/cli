import { Paginated } from './types/paginated';
import { ClientOptions, DEFAULT_OPTIONS } from './options';
import { Request, request, execute } from './request';
import { APIError, isAPIError } from './types';

export async function exec<K>(
    req: Request,
    validate: (data: any) => data is K
): Promise<K | APIError> {
    const { code, data } = await execute(req);
    if (isAPIError(data)) {
        const err = data as APIError;
        err.code = code;
        return err;
    }

    if (validate(data)) {
        return data as K;
    }

    throw new Error(
        `Unexpected server response for ${req.method} to ${
            req.endpoint
        }: ${JSON.stringify(data)}`
    );
}

type PusherFunction<T, K> = (
    options: ClientOptions,
    args: T
) => Promise<K | APIError>;

interface Model {
    id: string;
}

export function pusher<T, K>(
    endpoint: string,
    method: string,
    validate: (data: any) => data is K
): PusherFunction<T, K> {
    return async (options: ClientOptions, args: T): Promise<K | APIError> => {
        const req = request({
            options,
            method,
            endpoint,
            data: args
        });
        return await exec(req, validate);
    };
}

type DefaultPusherFunction<T, K> = (args: T) => Promise<K | APIError>;

export function defaultPush<T, K>(
    fn: PusherFunction<T, K>
): DefaultPusherFunction<T, K> {
    return async (args: T): Promise<K | APIError> => {
        return await fn(DEFAULT_OPTIONS, args);
    };
}

type ByIdFunction<K> = (
    options: ClientOptions,
    id: string
) => Promise<K | APIError>;

export function byId<K>(
    endpoint: string,
    validate: (data: any) => data is K,
    method?: string
): ByIdFunction<K> {
    return async (
        options: ClientOptions,
        id: string
    ): Promise<K | APIError> => {
        const req = request({
            options,
            endpoint: `${endpoint}/${id}`,
            method: method ? method : 'GET'
        });
        return await exec(req, validate);
    };
}

type DefaultByIdFunction<K> = (id: string) => Promise<K | APIError>;

export function defaultById<K>(fn: ByIdFunction<K>): DefaultByIdFunction<K> {
    return async (id: string): Promise<K | APIError> => {
        return await fn(DEFAULT_OPTIONS, id);
    };
}

type ListerFunction<K> = (options: ClientOptions) => Promise<K | APIError>;

export function lister<K>({
    endpoint,
    validate,
    limit = 50,
    offset = 0
}: {
    endpoint: string;
    validate: (data: any) => data is K;
    limit?: number;
    offset?: number;
}): ListerFunction<K> {
    return async (options: ClientOptions): Promise<K | APIError> => {
        const req = request({
            options,
            endpoint,
            method: 'GET',
            params: {
                limit,
                offset
            }
        });
        return await exec(req, validate);
    };
}

type DefaultListerFunction<K> = () => Promise<K | APIError>;

export function defaultList<K>(
    fn: ListerFunction<K>
): DefaultListerFunction<K> {
    return async (): Promise<K | APIError> => {
        return await fn(DEFAULT_OPTIONS);
    };
}

type DeleterFunction = (
    options: ClientOptions,
    id: string
) => Promise<null | APIError>;

export function deleter(endpoint: string): DeleterFunction {
    return async (
        options: ClientOptions,
        id: string
    ): Promise<null | APIError> => {
        const req = request({
            options,
            endpoint: `${endpoint}/${id}`,
            method: 'DELETE'
        });
        const data = await execute(req);
        if (isAPIError(data) && data.code >= 300) {
            return data as APIError;
        }

        return null;
    };
}

type DefaultDeleterFunction = (id: string) => Promise<null | APIError>;

export function defaultDelete(fn: DeleterFunction): DefaultDeleterFunction {
    return async (id: string): Promise<null | APIError> => {
        return await fn(DEFAULT_OPTIONS, id);
    };
}

export interface CRUD<CreateArgs, K> {
    listValidator: (data: any) => data is Paginated<K>;
    defaulted: {
        get: DefaultByIdFunction<K>;
        list: DefaultListerFunction<Paginated<K>>;
        update: DefaultPusherFunction<K, K>;
        create: DefaultPusherFunction<CreateArgs, K>;
        del: DefaultDeleterFunction;
    };
    optionable: {
        get: ByIdFunction<K>;
        list: ListerFunction<Paginated<K>>;
        update: PusherFunction<K, K>;
        create: PusherFunction<CreateArgs, K>;
        del: DeleterFunction;
    };
}

export function crud<CreateArgs, K>(
    endpoint: string,
    validate: (data: any) => data is K
): CRUD<CreateArgs, K> {
    const listValidator = (data: any): data is Paginated<K> => {
        return (
            data &&
            data.limit !== undefined &&
            data.offset !== undefined &&
            Array.isArray(data.data) &&
            data.data.every(validate)
        );
    };

    // Create
    const create = pusher<CreateArgs, K>(endpoint, 'POST', validate);
    // Read
    const get = byId<K>(endpoint, validate);
    const list = lister<Paginated<K>>({ endpoint, validate: listValidator });
    // Update
    const update = pusher<K, K>(endpoint, 'PUT', validate);
    // Delete
    const del = deleter(endpoint);

    return {
        listValidator,
        defaulted: {
            get: defaultById(get),
            list: defaultList(list),
            update: defaultPush(update),
            create: defaultPush(create),
            del: defaultDelete(del)
        },
        optionable: {
            get: get,
            list: list,
            update: update,
            create: create,
            del: del
        }
    };
}
