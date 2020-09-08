#!/bin/bash

if [ -z "$2" ]; then
    echo "Usage: $0 VERSION_NUMBER \"CHANGELOG_LINE1;CHANGELOG_LINE2;...\""
    exit
fi

AUTHOR='gabmus'
PROJECT_NAME=$(grep "project('" meson.build | sed "s/project('//;s/',//")


n_version="$1"
changelog="$2"

sed -i "s/    version: '.*',/    version: '$n_version',/" meson.build

MANIFEST_PATH="dist/flatpak/org.$AUTHOR.$PROJECT_NAME.json"
TARGET_MODULE="$PROJECT_NAME"

python3 -c "
import json
manifest = None
with open('$MANIFEST_PATH') as fd:
    manifest = json.loads(fd.read())
for i, module in enumerate(manifest['modules']):
    if module['name'] == '$TARGET_MODULE':
        manifest['modules'][i]['sources'][0]['tag'] = '$n_version'
        break
with open('$MANIFEST_PATH', 'w') as fd:
    fd.write(json.dumps(manifest, indent=4, sort_keys=False))
"

RELEASE_TIME=$(date +%s)

release_text=$(python3 -c "
def mprint(t):
    print(t, end='\\\\n')
mprint('        <release version=\"$n_version\" timestamp=\"$RELEASE_TIME\">')
mprint('            <description>')
mprint('                <ul>')
for line in '$changelog'.split(';'):
    mprint('                    <li>'+line.strip()+'</li>')
mprint('                </ul>')
mprint('            </description>')
mprint('        </release>')
")

APPDATA_PATH="data/org.$AUTHOR.$PROJECT_NAME.appdata.xml.in"

target_line=$(sed -n "/<releases/=" $APPDATA_PATH)

sed -i "${target_line}a\
$release_text" $APPDATA_PATH

sed -i "s~<release version=\"$n_version\" timestamp=\"$RELEASE_TIME\">~        <release version=\"$n_version\" timestamp=\"$RELEASE_TIME\">~" $APPDATA_PATH
