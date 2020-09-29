import path from 'path';
import kleur from 'kleur';
import { APIError, tasks, isAPIError } from './client';

export const emailRegex = /\S+@\S+\.\S+/;

export function fail(err: APIError): void {
    console.log(kleur.red('error:'), err.code, err.message);
    process.exit(err.code);
}

export function unexpected(err: Error): void {
    console.log(kleur.red('Unexpected error:'), err.toString());
    process.exit(1);
}

export async function highestPriority(): Promise<number> {
    try {
        const current = await tasks.current();
        if (isAPIError(current)) {
            if (current.code === 404) {
                return 2;
            }

            fail(current);
            return 0;
        }

        return current.priority;
    } catch (e) {
        unexpected(e);
        return 0;
    }
}

/**
 * Finds the platform-specific config dir
 *
 * @remarks
 * Follows the XDG specification for all platforms then will use a resonable
 * default based on platform.
 *
 */
export function configDir(): string {
    if (process.env.XDG_CONFIG_HOME) {
        return path.join(process.env.XDG_CONFIG_HOME, 'taskforge');
    }

    if (process.platform === 'win32') {
        return path.join(process.env.APPDATA!, 'Taskforge', 'config');
    }

    return path.join(process.env.HOME!, '.config', 'taskforge');
}

/**
 * Returns the platform-specific user data dir
 *
 * @remarks
 * Follows the XDG specification for all platforms then will use a resonable
 * default based on platform.
 *
 */
export function dataDir(): string {
    if (process.env.XDG_DATA_HOME) {
        return path.join(process.env.XDG_DATA_HOME, 'taskforge');
    }

    if (process.platform === 'win32') {
        return path.join(process.env.APPDATA!, 'Taskforge', 'data');
    }

    return path.join(process.env.HOME!, '.local', 'share', 'taskforge');
}
