export interface Paginated<T> {
    limit: number;
    offset: number;
    data: T[];
}
