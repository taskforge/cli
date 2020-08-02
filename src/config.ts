import path from 'path';
import YAML from 'yaml';
import { existsSync, readFileSync } from 'fs';

import { configDir } from './utils';

const CONFIG = {};

const CONFIG_FILE_LOCATIONS = [
    'Taskforge.yaml',
    'Taskforge.yml',
    path.join(configDir(), 'config.yaml')
];

function loadConfigFile(): void {
    let fp: string | undefined;
    for (const location in CONFIG_FILE_LOCATIONS) {
        if (existsSync(location)) {
            fp = location;
            break;
        }
    }

    if (!fp) {
        return;
    }

    const data = readFileSync(fp);
    Object.assign(CONFIG, YAML.parse(data.toString('utf-8')));
}

loadConfigFile();
export default CONFIG;
