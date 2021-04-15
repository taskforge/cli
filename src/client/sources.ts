import { ModelClient, isAPIError } from './model-client';

export interface Source {
    id: string;
    name: string;
}

export function isSource(data: any): data is Source {
    return (
        data !== undefined && data.id !== undefined && data.name !== undefined
    );
}

export class SourceClient extends ModelClient<Source, Source> {
    pluralName = 'sources';
    validator = (data: any): Source => {
        if (!isSource(data)) {
            throw new Error('Got unexpcted Setting data!');
        }

        return data;
    };

    async byName(name: string): Promise<Source> {
        const url = `/${this.version}/${this.pluralName}`;
        const response = await this.client.get(url, { params: { name } });
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return this.validator(response.data);
    }
}
