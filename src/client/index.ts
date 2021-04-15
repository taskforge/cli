import { CommentClient } from './comments';
import { ContextClient } from './contexts';
import { FilterClient } from './filters';
import { SettingClient } from './settings';
import { SourceClient } from './sources';
import { TaskClient } from './tasks';
import { UserClient } from './users';

export class Client {
    filters: FilterClient;
    sources: SourceClient;
    comments: CommentClient;
    users: UserClient;
    settings: SettingClient;
    contexts: ContextClient;
    tasks: TaskClient;

    constructor(token: string, baseUrl: string) {
        this.comments = new CommentClient(token, baseUrl);
        this.contexts = new ContextClient(token, baseUrl);
        this.filters = new FilterClient(token, baseUrl);
        this.settings = new SettingClient(token, baseUrl);
        this.sources = new SourceClient(token, baseUrl);
        this.tasks = new TaskClient(token, baseUrl);
        this.users = new UserClient(token, baseUrl);
    }
}

const client = new Client(
    process.env.TASKFORGE_TOKEN as string,
    process.env.TASKFORGE_HOST as string
);

export default client;
