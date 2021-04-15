import { ModelClient, isAPIError } from './model-client';

export interface Column {
    name: string;
    enabled: boolean;
}

export function isColumn(data: any): data is Column {
    return data.name && data.enabled !== undefined;
}

export interface Filter {
    id: string;

    name: string;
    query: string;

    columns: Column[];

    owner: string;
}

export interface NewFilter {
    name: string;
    query: string;
    columns?: Column[];
}

export function isFilter(data: any): data is Filter {
    return (
        data &&
        data.id !== undefined &&
        data.name !== undefined &&
        data.query !== undefined &&
        data.columns.every(isColumn) &&
        data.owner !== undefined
    );
}

export class FilterClient extends ModelClient<Filter, NewFilter> {
    pluralName = 'tasks';
    validator = (data: any): Filter => {
        if (!isFilter(data)) {
            throw new Error('Got unexpcted Filter data!');
        }

        return data;
    };

    async byName(name: string): Promise<Filter> {
        const url = `/${this.version}/${this.pluralName}`;
        const response = await this.client.get(url, { params: { name } });
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return this.validator(response.data);
    }
}
