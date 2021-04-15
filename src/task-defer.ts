import client from './client';
import { unexpected } from './utils';
import { Command } from 'commander';

async function defer() {
    try {
        const task = await client.tasks.get('next');
        await client.tasks.update({
            ...task,
            priority: task.priority - 1
        });
    } catch (e) {
        unexpected(e);
    }
}

export const DeferCommand = new Command('defer')
    .description("defer the current task by reducing it's priority")
    .action(defer);
