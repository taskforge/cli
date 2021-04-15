import { ModelClient, isAPIError } from './model-client';

export interface User {
    id: string;
    email: string;
    avatarUrl: string;

    fullName?: string;
}

export interface NewUser {
    email: string;
    password: string;
    fullName?: string;
}

export function isUser(data: any): data is User {
    return (
        data !== undefined &&
        data.id !== undefined &&
        data.email !== undefined &&
        data.avatarUrl !== undefined
    );
}

export interface Credentials {
    access: string;
    refresh: string | undefined;
}

export function isCredentials(data: any): data is Credentials {
    return data && data.access;
}

export interface PAT {
    pat: string;
}

export function isPAT(data: any): data is PAT {
    return data && data.pat;
}

export class UserClient extends ModelClient<User, NewUser> {
    pluralName = 'users';
    validator = (data: any): User => {
        if (!isUser(data)) {
            throw new Error('Got unexpcted Setting data!');
        }

        return data;
    };

    async login(email: string, password: string): Promise<Credentials> {
        const url = `/${this.version}/tokens`;
        const response = await this.client.post(url, {
            email,
            password
        });
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        if (!isCredentials(response.data)) {
            throw new Error('Unexpected response for tokens!');
        }

        return response.data;
    }

    async generatePAT(email: string, password: string): Promise<PAT> {
        const url = `/${this.version}/tokens/pat`;
        const response = await this.client.post(url, {
            email,
            password
        });
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        if (!isPAT(response.data)) {
            throw new Error('Unexpected response for tokens!');
        }

        return response.data;
    }
}
