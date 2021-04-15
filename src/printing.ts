import client from './client';
import { Task } from './client/tasks';
import { table } from 'table';

function idMemo<T>(fn: (id: string) => Promise<T>): (id: string) => Promise<T> {
    const memo: { [id: string]: T } = {};
    return async (id: string): Promise<T> => {
        if (memo[id]) {
            return memo[id];
        }

        const model = await fn(id);
        return model;
    };
}

const getContext = idMemo(client.contexts.get);
const getSource = idMemo(client.sources.get);
const getUser = idMemo(client.users.get);

function humanizeKey(key: string): string {
    if (key == 'id') {
        return 'ID';
    }

    const words = key.match(/[A-Za-z][a-z]*/g) || [];
    return words
        .map((word) => {
            return word.charAt(0).toUpperCase() + word.substring(1);
        })
        .join(' ');
}

async function humanize(task: Task): Promise<any> {
    const [context, source, owner] = await Promise.all([
        getContext(task.context),
        getSource(task.source),
        getUser(task.owner)
    ]);
    return {
        ...task,
        owner:
            owner.fullName && owner.fullName !== ''
                ? owner.fullName
                : owner.email,
        context: context.name,
        source: source.name
    };
}

export async function printTable(list: Task[]): Promise<void> {
    const headers = [
        'id',
        'title',
        'priority',
        'createdDate',
        'completedDate',
        'source',
        'context',
        'owner'
    ];
    const data: any[][] = [headers.map(humanizeKey)];

    for (const task of await Promise.all(list.map(humanize))) {
        data.push(
            headers.map((key) => {
                const value = task[key];
                if (value === undefined || value === null) {
                    return 'null';
                }
                return value;
            })
        );
    }

    const options = {
        drawHorizontalLine: (index: number, size: number) => {
            return index === 0 || index === 1 || index === size;
        }
    };

    console.log(table(data, options));
}

export function printJSON(obj: any): void {
    console.log(JSON.stringify(obj, null, 2));
}

export function printList(list: Task[], format: string): void {
    switch (format) {
        case 'json':
            printJSON(list);
            break;
        default:
            if (list.length === 0) {
                console.log('No tasks to show!');
                return;
            }

            printTable(list);
    }
}

export async function printTask(task: Task): Promise<void> {
    const humanized = await humanize(task);
    const data: any[][] = Object.keys(humanized).map((key) => {
        return [humanizeKey(key), humanized[key] ? humanized[key] : 'null'];
    });

    console.log(table(data));
}
