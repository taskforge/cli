import { request } from '../request';
import {
    APIError,
    isContext,
    Context,
    isAPIError,
    isPaginated
} from '../types';
import { exec, crud } from '../generate';
import { ClientOptions, DEFAULT_OPTIONS } from '../options';

export interface ContextCreateArgs {
    name: string;
}

const { defaulted, optionable } = crud<ContextCreateArgs, Context>(
    '/v1/contexts',
    isContext
);

const byNameWithOptions = async (
    options: ClientOptions,
    name: string
): Promise<Context | APIError> => {
    const req = request({
        options,
        endpoint: `/v1/contexts?name=${name}`,
        method: 'GET'
    });

    const res = await exec(req, isPaginated(isContext));
    if (isAPIError(res)) {
        return res;
    }

    return res.results[0];
};

const byName = async (name: string): Promise<Context | APIError> => {
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
