import { CommentClient } from './comments';
import { ContextClient } from './contexts';
import { FilterClient } from './filters';
import { SettingClient } from './settings';
import { SourceClient } from './sources';
import { TaskClient } from './tasks';
import { UserClient } from './users';
import axios, { AxiosInstance } from 'axios';

export class Client {
    client: AxiosInstance;
    filters: FilterClient;
    sources: SourceClient;
    comments: CommentClient;
    users: UserClient;
    settings: SettingClient;
    contexts: ContextClient;
    tasks: TaskClient;

    constructor(token: string, baseUrl: string) {
        this.client = axios.create({
            baseURL: baseUrl,
            headers: { authorization: `Bearer ${token}` }
        });

        this.comments = new CommentClient(this.client);
        this.contexts = new ContextClient(this.client);
        this.filters = new FilterClient(this.client);
        this.settings = new SettingClient(this.client);
        this.sources = new SourceClient(this.client);
        this.tasks = new TaskClient(this.client);
        this.users = new UserClient(this.client);
    }
}

const client = new Client(
    process.env.TASKFORGE_TOKEN as string,
    process.env.TASKFORGE_HOST as string
);

export default client;
