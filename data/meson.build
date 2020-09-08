app_id = '.'.join([
    domain,
    author,
    meson.project_name()
])

app_id_aspath = '/'.join([
    domain,
    author,
    meson.project_name()
])

desktop_conf = configuration_data()
desktop_conf.set('bindir', join_paths(prefix, bindir))
desktop_conf.set('prettyname', prettyname)
# .desktop comment now hardcoded for better i18n support
#desktop_conf.set('description', description)
desktop_conf.set('appid', app_id)
desktop_conf.set('projectname', meson.project_name())

desktop_file = configure_file(
    input: app_id + '.desktop.in',
    output: app_id + '.desktop.i18n.in',
    configuration: desktop_conf
)

i18n.merge_file(
    input: desktop_file,
    output: app_id + '.desktop',
    po_dir: '../po',
    type: 'desktop',
    install: true,
    install_dir: join_paths(datadir, 'applications')
)

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif
dependency('glib-2.0')
dependency('gobject-introspection-1.0', version: '>=1.35.9')
dependency('gtk+-3.0', version :'>=3.20')

dbus_conf = configuration_data()
dbus_conf.set('bindir', join_paths(prefix, bindir))
dbus_conf.set('appid', app_id)
dbus_conf.set('projectname', meson.project_name())

configure_file(
    input: app_id + '.service.in',
    output: app_id + '.service',
    configuration: dbus_conf,
    install_dir: join_paths(datadir, 'dbus-1/services')
)

gschema_conf = configuration_data()
gschema_conf.set('apppath', app_id_aspath)
gschema_conf.set('appid', app_id)
gschema_conf.set('projectname', meson.project_name())

configure_file(
    input: app_id + '.gschema.xml.in',
    output: app_id + '.gschema.xml',
    configuration: gschema_conf,
    install_dir: join_paths(datadir, 'glib-2.0/schemas')
)

icondir = join_paths(datadir, 'icons/hicolor')
install_data(
    'icons/'+app_id+'.svg',
    install_dir: join_paths(icondir, 'scalable/apps')
)
install_data(
    'icons/'+app_id+'-symbolic.svg',
    install_dir: join_paths(icondir, 'symbolic/apps')
)

subdir('ui')

app_resources = gnome.compile_resources(app_id,
    app_id + '.gresource.xml',
    gresource_bundle: true,
    dependencies: configure_file(
        input: 'ui/aboutdialog.glade.in',
        output: 'aboutdialog.glade',
        configuration: glade_conf
    ),
    install: true,
    install_dir: pkgdatadir
)

app_settings = gnome.compile_schemas()

#appdata_conf = configuration_data()
#appdata_conf.set('authorfullname', authorfullname)
#appdata_conf.set('gitrepo', gitrepo)
#appdata_conf.set('website', website)
#appdata_conf.set('authoremail', authoremail)
#appdata_conf.set('prettyname', prettyname)
#appdata_conf.set('appid', app_id)
#appdata_conf.set('prettylicense', prettylicense)
#
#configure_file(
#    input: appdata_file,
#    output: app_id + '.appdata.xml.',
#    configuration: appdata_conf,
#    install: true,
#    install_dir: join_paths(datadir, 'metainfo')
#)

ascli_exe = find_program('appstreamcli', required: false)
if ascli_exe.found()
    test(
        'validate metainfo file',
        ascli_exe,
        args: [
            'validate',
            #'--no-net',
            #'--pedantic',
            'data/' + app_id + '.appdata.xml'
        ]
    )
endif

i18n.merge_file(
    input: app_id + '.appdata.xml.in',
    output: app_id + '.appdata.xml',
    po_dir: '../po',
    install: true,
    install_dir: join_paths(datadir, 'metainfo')
)
