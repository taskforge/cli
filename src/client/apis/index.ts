import comments, { withOptions as commentsWithOptions } from './comments';
import contexts, { withOptions as contextsWithOptions } from './contexts';
import filters, { withOptions as filtersWithOptions } from './filters';
import sources, { withOptions as sourcesWithOptions } from './sources';
import tasks, { withOptions as tasksWithOptions } from './tasks';
import users, { withOptions as usersWithOptions } from './users';

export const withOptions = {
    comments: commentsWithOptions,
    contexts: contextsWithOptions,
    filters: filtersWithOptions,
    sources: sourcesWithOptions,
    tasks: tasksWithOptions,
    users: usersWithOptions
};

export default { comments, contexts, filters, sources, tasks, users };
