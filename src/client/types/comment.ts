export interface Comment {
    id: string;
    author: string;
    body: string;
    object: string;
    createdDate: Date;
}

export function isComment(data: any): data is Comment {
    return (
        data &&
        data.id &&
        data.author &&
        data.body &&
        data.object &&
        data.createdDate
    );
}
