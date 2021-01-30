import { request } from '../request';
import { exec, defaultById, crud } from '../generate';
import { ClientOptions, DEFAULT_OPTIONS } from '../options';
import { APIError, isAPIError, isTask, Task } from '../types';
import { Paginated } from '../types/paginated';

export interface TaskCreateArgs {
    title: string;

    owner?: string;
    source?: string;
    priority?: number;
    context?: string;
}

export interface NextOptions {
    context?: string;
}

const { listValidator, defaulted, optionable } = crud<TaskCreateArgs, Task>(
    '/v1/tasks',
    isTask
);

const currentWithOptions = async (
    options: ClientOptions,
    opts?: NextOptions
): Promise<Task | APIError> => {
    let endpoint = `/v1/tasks/next`;
    if (opts && opts.context) {
        endpoint += `?context=${opts.context}`;
    }

    const req = request({
        options,
        endpoint,
        method: 'GET'
    });
    return await exec(req, isTask);
};

const current = async (opts?: NextOptions): Promise<Task | APIError> => {
    return await currentWithOptions(DEFAULT_OPTIONS, opts);
};

const completeWithOptions = async (
    options: ClientOptions,
    id: string
): Promise<null | APIError> => {
    const req = request({
        options,
        endpoint: `/v1/tasks/${id}`,
        method: 'PUT'
    });

    const res = await exec(req, (data: any): data is null => data || true);
    if (isAPIError(res) && res.code == 200) {
        return null;
    }

    return res;
};

const complete = defaultById(completeWithOptions);

const searchWithOptions = async (
    options: ClientOptions,
    query: string
): Promise<Paginated<Task> | APIError> => {
    const req = request({
        options,
        endpoint: `/v1/tasks?query=${query}`,
        method: 'GET'
    });
    return await exec(req, listValidator);
};

const search = async (query: string): Promise<Paginated<Task> | APIError> => {
    return await searchWithOptions(DEFAULT_OPTIONS, query);
};

export const withOptions = {
    ...optionable,
    complete: completeWithOptions,
    search: searchWithOptions,
    current: currentWithOptions
};

export default { ...defaulted, current, complete, search };
