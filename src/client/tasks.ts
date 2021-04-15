import { ModelClient, isAPIError } from './model-client';

export interface Task {
    id: string; // UUID

    title: string;

    owner: string; // UUID

    source: string;
    priority: number;
    context: string;

    createdDate: string | Date;
    completedDate: string | Date | null;
}

export interface NewTask {
    title: string;

    priority?: number;
    context?: string;
}

export function isTask(data: any): data is Task {
    return (
        data &&
        data.title !== undefined &&
        data.owner !== undefined &&
        data.source !== undefined &&
        data.priority !== undefined &&
        data.context !== undefined &&
        data.createdDate !== undefined
    );
}

export class TaskClient extends ModelClient<Task, NewTask> {
    pluralName = 'tasks';
    validator = (data: any): Task => {
        if (!isTask(data)) {
            throw new Error('Got unexpcted Task data!');
        }

        return data;
    };

    async search(query: string): Promise<Task[]> {
        return await this.list(0, { query });
    }

    async complete(id: string): Promise<Task> {
        const url = `/${this.version}/${this.pluralName}/${id}`;
        const response = await this.client.put(url);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return this.validator(response.data);
    }

    async next(context?: string): Promise<Task> {
        const url = context
            ? `/${this.version}/${this.pluralName}/next?context=${context}`
            : `/${this.version}/${this.pluralName}/next`;
        const response = await this.client.get(url);
        if (isAPIError(response.data)) {
            throw new Error(response.data.message);
        }

        return this.validator(response.data);
    }
}
