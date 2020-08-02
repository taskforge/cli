import path from 'path';
import { promises as fs } from 'fs';

import { dataDir } from './utils';

export interface State {
    currentContext?: string;
}

/**
 * Returns the path to the application state file.
 *
 */
function stateFile(): string {
    return path.join(dataDir(), 'state.json');
}

/**
 * Load the application state from the stateFile
 *
 */
export async function loadState(): Promise<State> {
    try {
        const fn = stateFile();
        await fs.stat(fn);
        const data = await fs.readFile(fn);
        return JSON.parse(data.toString('utf-8')) as State;
    } catch {
        return {};
    }
}

/**
 * Save the given state to the stateFile
 *
 * @param state - State object to be saved
 *
 */
export async function saveState(state: State): Promise<void> {
    try {
        await fs.stat(dataDir());
    } catch {
        await fs.mkdir(dataDir(), { recursive: true });
    }

    const data = JSON.stringify(state);
    await fs.writeFile(stateFile(), data);
}
