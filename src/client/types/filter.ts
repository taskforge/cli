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

    showCompleted: boolean;
    columns: Column[];

    owner: string;
}

export function isFilter(data: any): data is Filter {
    return (
        data &&
        data.id &&
        data.name &&
        data.query &&
        data.showCompleted !== undefined &&
        data.columns.every(isColumn) &&
        data.owner
    );
}
