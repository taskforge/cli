import { AxiosInstance } from 'axios';

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
    version: string;
    client: AxiosInstance;
    abstract validator: (data: any) => Model;
    abstract pluralName: string;

    constructor(client: AxiosInstance, version = 'v1') {
        this.version = version;
        this.client = client;
    }

    isPaginated(data: any): Paginated<Model> {
        return (
            data.offset !== undefined &&
            data.limit !== undefined &&
            data.results.map(this.validator)
        );
    }

    handleError(e: any) {
        if (isAPIError(e.response.data)) {
            throw new Error(e.response.data.message);
        }
    }

    async get(id: string): Promise<Model> {
        const url = `/${this.version}/${this.pluralName}/${id}`;
        try {
            const response = await this.client.get(url);
            return this.validator(response.data);
        } catch (e) {
            this.handleError(e);
            throw e;
        }
    }

    async list(offset = 0, queryParams?: any): Promise<Model[]> {
        try {
            const url = `/${this.version}/${this.pluralName}`;
            const options = queryParams
                ? { params: { offset, ...queryParams } }
                : { params: { offset } };
            const response = await this.client.get(url, options);
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
        } catch (e) {
            this.handleError(e);
            throw e;
        }
    }

    async create(model: NewModel): Promise<Model> {
        try {
            const url = `/${this.version}/${this.pluralName}`;
            const response = await this.client.post(url, model);
            return this.validator(response.data);
        } catch (e) {
            this.handleError(e);
            throw e;
        }
    }

    async update(model: Model): Promise<Model> {
        try {
            const url = `/${this.version}/${this.pluralName}`;
            const response = await this.client.put(url, model);
            return response.data;
        } catch (e) {
            this.handleError(e);
            throw e;
        }
    }

    async del(id: string): Promise<Model> {
        try {
            const url = `/${this.version}/${this.pluralName}/${id}`;
            const response = await this.client.delete(url);
            return response.data;
        } catch (e) {
            this.handleError(e);
            throw e;
        }
    }
}
