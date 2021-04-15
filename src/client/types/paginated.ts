export interface Paginated<T> {
    limit: number;
    offset: number;
    results: T[];
}

export function isPaginated<T>(
    isModel: (data: any) => data is T
): (data: any) => data is Paginated<T> {
    return (data: any): data is Paginated<T> => {
        return (
            data &&
            data.limit !== undefined &&
            data.offset !== undefined &&
            Array.isArray(data.results) &&
            data.results.every(isModel)
        );
    };
}
