import { isSource, Source } from '../types';
import { crud } from '../generate';

export interface SourceCreateArgs {
    name: string;
}

const { defaulted, optionable } = crud<SourceCreateArgs, Source>(
    '/v1/sources',
    isSource
);

export const withOptions = {
    get: optionable.get,
    list: optionable.list
};

export default {
    get: defaulted.get,
    list: defaulted.list
};
