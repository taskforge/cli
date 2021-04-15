import { Column } from './filters';
import { ModelClient } from './model-client';

export interface Settings {
    user: string;
    default_columns: Column[];
    default_context: string | null;
}

export function isSettings(data: any): data is Settings {
    return (
        data !== undefined &&
        data.user !== undefined &&
        data.default_columns !== undefined &&
        Array.isArray(data.default_columns) &&
        data.default_context !== undefined
    );
}

export class SettingClient extends ModelClient<Settings, Settings> {
    pluralName = 'settings';
    validator = (data: any): Settings => {
        if (!isSettings(data)) {
            throw new Error('Got unexpcted Setting data!');
        }

        return data;
    };
}
