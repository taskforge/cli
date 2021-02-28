import { isComment, APIError, Comment } from '../types';
import { ClientOptions, DEFAULT_OPTIONS } from '../options';
import { lister, pusher } from '../generate';
import { isPaginated, Paginated } from '../types/paginated';

export interface CommentCreateArgs {
    body: string;
}

const listWithOptions = async (
    options: ClientOptions,
    task: string
): Promise<Paginated<Comment> | APIError> => {
    const endpoint = `/v1/comments?object=${task}`;
    return lister<Paginated<Comment>>({
        endpoint,
        validate: isPaginated(isComment)
    })(options);
};

const list = async (task: string): Promise<Paginated<Comment> | APIError> => {
    return listWithOptions(DEFAULT_OPTIONS, task);
};

const createWithOptions = async (
    options: ClientOptions,
    task: string,
    comment: CommentCreateArgs
): Promise<Comment | APIError> => {
    const endpoint = `/v1/tasks/${task}/comments`;
    return pusher<CommentCreateArgs, Comment>(
        endpoint,
        'POST',
        isComment
    )(options, comment);
};

const create = async (
    task: string,
    comment: CommentCreateArgs
): Promise<Comment | APIError> => {
    return createWithOptions(DEFAULT_OPTIONS, task, comment);
};

export const withOptions = {
    list: listWithOptions,
    create: createWithOptions
};

export default {
    list,
    create
};
