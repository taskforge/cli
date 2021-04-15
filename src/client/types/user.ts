export interface User {
    id: string;
    email: string;
    avatarUrl: string;

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
