import sys
import os
import logging
import shutil
import datetime
import re
import json

import yaml

APP_NAME = os.path.basename(__file__)
APP_DIR = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
logger = logging.getLogger(APP_NAME)

KARABINER_JSON_FILE = '~/.config/karabiner/karabiner.json'
KARABINER_CMOD_DIR = '~/.config/karabiner/assets/complex_modifications'

def parse_args(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--setting-file','-f', default=KARABINER_JSON_FILE)
    parser.add_argument('--test','-t', action='store_true', default=False)
    parser.add_argument('files', metavar='FILEs...', nargs='+')
    return parser.parse_args(args=args)

def main(args):
    setting_file = os.path.expanduser(args.setting_file)
    logger.info(f"setting file: '{setting_file}'")
    
    with open(setting_file) as f:
        setting = json.load(f)
    profile = setting['profiles'][0]

    profile_rules = profile['complex_modifications']['rules'] = []

    for cm_file in args.files:
        cm_file = os.path.expanduser(cm_file)

        try:
            logger.info(f"cmod file: '{cm_file}'")
            with open(cm_file) as f:
                cm_obj = yaml.load(f, Loader=yaml.SafeLoader)

            desc_prefix = ""
            if cm_file_title := cm_obj.get("title"):
                desc_prefix = f"[{cm_file_title}] "

            rules = cm_obj['rules']
            for rule in rules:
                if desc_prefix:
                    rule["description"] = desc_prefix + rule["description"]
                logger.info(f"add rule: '{rule['description']}'")
                profile_rules.append(rule)
            
            cm_dest_json_file = os.path.expanduser(os.path.join(
                KARABINER_CMOD_DIR,
                re.sub(r'\.[^\.]+$','.json', os.path.basename(cm_file)),
            ))

            cm_obj = {k: v for k, v in cm_obj.items() if not k.startswith("_")}

            with open(cm_dest_json_file,'w') as f:
                json.dump(cm_obj, f, indent=2)
                logger.info(f"wrote cmod file: '%s'", cm_dest_json_file)
        except Exception as e:
            logger.error(f"error in file:'{cm_file}'", e)
            return 1

    modified_setting_json = json.dumps(setting,indent=2)
    
    if args.test:
        json.dump(setting, sys.stdout, indent=2)
        return 1
    
    backup_setting_file = "/tmp/karabiner-setting-backup/karabiner.%s.json" % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if not os.path.exists(os.path.dirname(backup_setting_file)):
        os.makedirs(os.path.dirname(backup_setting_file))
    shutil.copyfile(setting_file, backup_setting_file)
    
    with open(setting_file,'w') as f:
        json.dump(setting, f, indent=2)
        logger.info(f"wrote setting file: '{setting_file}' (backup: '{backup_setting_file}')")
    
    return 0

if __name__=='__main__':
    def configure_logger(logger):
        log_level = logging.INFO
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.addHandler(handler)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger.setLevel(log_level)
    configure_logger(logger)
    try:
        sys.exit(main(parse_args(sys.argv[1:])))
    except Exception as e:
        logger.exception(f'{APP_NAME} failed.')
