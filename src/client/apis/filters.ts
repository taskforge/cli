import { request } from '../request';
import { isFilter, Filter, APIError } from '../types';
import { exec, crud } from '../generate';
import { ClientOptions, DEFAULT_OPTIONS } from '../options';

export interface Column {
    name: string;
    enabled: boolean;
}

export interface FilterCreateArgs {
    name: string;
    query: string;
    show_completed?: boolean;
    columns?: Column[];
}

const { defaulted, optionable } = crud<FilterCreateArgs, Filter>(
    '/v1/filters',
    isFilter
);

const byNameWithOptions = async (
    options: ClientOptions,
    name: string
): Promise<Filter | APIError> => {
    const req = request({
        options,
        endpoint: `/v1/filters?name=${name}`,
        method: 'GET'
    });

    return await exec(req, isFilter);
};

const byName = async (name: string): Promise<Filter | APIError> => {
    return await byNameWithOptions(DEFAULT_OPTIONS, name);
};

export const withOptions = {
    ...optionable,
    byName: byNameWithOptions
};

export default {
    ...defaulted,
    byName
};
