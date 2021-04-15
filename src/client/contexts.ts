import { ModelClient, isAPIError } from './model-client';

export interface Context {
    id: string;
    name: string;
    owner: string;
}

export interface NewContext {
    name: string;
}

export function isContext(data: any): data is Context {
    return data && data.id && data.name && data.owner !== undefined;
}

export class ContextClient extends ModelClient<Context, NewContext> {
    pluralName = 'tasks';
    validator = (data: any): Context => {
        if (!isContext(data)) {
            throw new Error('Got unexpcted Context data!');
        }

        return data;
    };

    async byName(name: string): Promise<Context> {
        const url = `/${this.version}/${this.pluralName}`;
        const response = await this.client.get(url, { params: { name } });
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return this.validator(response.data);
    }
}
