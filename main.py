import os
from airplane_data import run
import yaml


def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main():
    config = load_config('config.yaml')

    run(
        config['base_url'],
        config['download_dir'],
        os.path.join(config['data_dir'], config['output_file']),
        config['r_script_path'],
        (config['start_year'], config['start_month']),
        (config['end_year'], config['end_month'])
    )


if __name__ == "__main__":
    main()
