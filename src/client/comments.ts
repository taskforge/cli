import { ModelClient, isAPIError } from './model-client';

export interface Comment {
    id: string;
    author: string;
    body: string;
    object: string;
    createdDate: Date;
}

export interface NewComment {
    body: string;
    object: string;
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

export class CommentClient extends ModelClient<Comment, NewComment> {
    pluralName = 'tasks';
    validator = (data: any): Comment => {
        if (!isComment(data)) {
            throw new Error('Got unexpcted Comment data!');
        }

        return data;
    };

    async list(offset = 0, id?: string, queryParams?: any): Promise<Comment[]> {
        const url = `/${this.version}/${this.pluralName}`;
        const options = queryParams
            ? { params: { offset, object: id } }
            : { params: { offset, object: id, ...queryParams } };
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
                id
            );
            return [...results, ...nextPage];
        }

        return results;
    }
}
