export interface Source {
    id: string;
    name: string;
}

export function isSource(data: any): data is Source {
    return data && data.id && data.name;
}
