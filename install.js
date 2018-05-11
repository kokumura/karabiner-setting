const fs = require("fs");
const path = require('path');
const util = require('util');
const strftime = require('strftime');
const program = require("commander");
const CSON = require("cson");
const expandTilde = require('expand-tilde');

const KARABINER_JSON_FILE = '~/.config/karabiner/karabiner.json';
const KARABINER_CMOD_DIR = '~/.config/karabiner/assets/complex_modifications';

program
  .usage('')
  .option('-t, --test')
  .option('-f, --setting-file [file]', 'karabiner.json file', KARABINER_JSON_FILE)
  .parse(process.argv);

program.parse(process.argv);
const settingFilePath = expandTilde(program.settingFile);
if(settingFilePath === undefined){
  program.help();
}
console.log("setting file: "+settingFilePath);
const cmFiles = program.args;

var origSettingJSON = fs.readFileSync(settingFilePath,'utf8');
var setting = JSON.parse(origSettingJSON);
var profile = setting.profiles[0];
profile.complex_modifications.rules = [];

for(var cmFile of cmFiles){
  var cmObj = CSON.parse(fs.readFileSync(expandTilde(cmFile),'utf8'));
  if(cmObj.rules){
    console.log(util.format("cmod file: %s", path.basename(cmFile)));
    for(var rule of cmObj.rules){
      console.log(util.format("add rule: '%s'", rule.description));
      profile.complex_modifications.rules.push(rule);
    }
    var cmJsonFile = expandTilde(KARABINER_CMOD_DIR + "/" + path.basename(cmFile).replace(".cson",".json"));
    fs.writeFileSync(cmJsonFile,JSON.stringify(cmObj,null,2),'utf8');
    console.log(util.format("wrote cmod file: '%s'", cmJsonFile));
  } else {
    console.log(cmObj);
    console.error(`CSON parse error in '${cmFile}'`);
    process.exit(1);
  }
}

var modifiedSettingJSON = JSON.stringify(setting,null,2);

if(program.test){
  process.stdout.write(modifiedSettingJSON);
} else {
  var backupFilePath = util.format("backup/karabiner.%s.json",strftime('%Y%m%d%H%M%S'));
  if (!fs.existsSync(path.dirname(backupFilePath))){
    fs.mkdirSync(path.dirname(backupFilePath));
  }
  fs.writeFileSync(backupFilePath,origSettingJSON,'utf8');
  fs.writeFileSync(settingFilePath,modifiedSettingJSON,'utf8');
  console.log(util.format("wrote setting file: '%s' (backup: '%s')", settingFilePath, backupFilePath));
}



