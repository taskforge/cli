import axios, { AxiosInstance } from 'axios';

export interface APIError {
    code: number;
    message?: string;
}

export function isAPIError(data: any): data is APIError {
    return (
        data &&
        data.code !== undefined &&
        (data.detail !== undefined || data.message !== undefined)
    );
}

export interface Paginated<T> {
    limit: number;
    offset: number;
    results: T[];
}

export abstract class ModelClient<Model, NewModel> {
    version = 'v1';
    client: AxiosInstance;
    abstract validator: (data: any) => Model;
    abstract pluralName: string;

    constructor(token: string, baseUrl: string) {
        this.client = axios.create({
            baseURL: baseUrl,
            headers: { authorization: `Bearer ${token}` }
        });
    }

    isPaginated(data: any): Paginated<Model> {
        return (
            data.offset !== undefined &&
            data.limit !== undefined &&
            data.results.map(this.validator)
        );
    }

    async get(id: string): Promise<Model> {
        const url = `/${this.version}/${this.pluralName}/${id}`;
        const response = await this.client.get(url);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return this.validator(response.data);
    }

    async list(offset = 0, queryParams?: any): Promise<Model[]> {
        const url = `/${this.version}/${this.pluralName}`;
        const options = queryParams
            ? { params: { offset } }
            : { params: { offset, ...queryParams } };
        const response = await this.client.get(url, options);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        if (!this.isPaginated(response.data)) {
            throw new Error(`Unexpected response from ${url}`);
        }

        const results = response.data.results.map(this.validator);
        if (response.data.limit == results.length) {
            const nextPage = await this.list(
                response.data.offset + response.data.limit,
                options
            );
            return [...results, ...nextPage];
        }

        return results;
    }

    async create(model: NewModel): Promise<Model> {
        const url = `/${this.version}/${this.pluralName}`;
        const response = await this.client.post(url, model);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return response.data;
    }

    async update(model: Model): Promise<Model> {
        const url = `/${this.version}/${this.pluralName}`;
        const response = await this.client.put(url, model);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return response.data;
    }

    async del(id: string): Promise<Model> {
        const url = `/${this.version}/${this.pluralName}/${id}`;
        const response = await this.client.delete(url);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return response.data;
    }
}
