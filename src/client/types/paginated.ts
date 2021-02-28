export interface Paginated<T> {
    count: number;
    previous: string | null;
    next: string | null;
    results: T[];
}

export function isPaginated<T>(
    isModel: (data: any) => data is T
): (data: any) => data is Paginated<T> {
    return (data: any): data is Paginated<T> => {
        return (
            data &&
            data.next !== undefined &&
            data.previous !== undefined &&
            data.count !== undefined &&
            Array.isArray(data.results) &&
            data.results.every(isModel)
        );
    };
}
