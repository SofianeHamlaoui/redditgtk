# from os import remove, listdir
# from os.path import isfile, abspath, join
from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.confManager import ConfManager


class PreferencesButtonRow(Handy.ActionRow):
    """
    A preferences row with a title and a button
    title: the title shown
    button_label: a label to show inside the button
    onclick: the function that will be called when the button is pressed
    button_style_class: the style class of the button.
        Common options: `suggested-action`, `destructive-action`
    signal: an optional signal to let ConfManager emit when the button is
        pressed
    """
    def __init__(self, title, button_label, onclick, button_style_class=None,
                 signal=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.button_label = button_label
        self.confman = ConfManager()
        self.set_title(self.title)
        self.signal = signal
        self.onclick = onclick

        self.button = Gtk.Button()
        self.button.set_label(self.button_label)
        self.button.set_valign(Gtk.Align.CENTER)
        if button_style_class:
            self.button.get_style_context().add_class(button_style_class)
        self.button.connect('clicked', self.on_button_clicked)
        self.add(self.button)
        # You need to press the actual button
        # Avoids accidental presses
        # self.set_activatable_widget(self.button)

    def on_button_clicked(self, button):
        self.onclick(self.confman)
        if self.signal:
            self.confman.emit(self.signal, '')
        self.confman.save_conf()


class PreferencesFileChooserRow(Handy.ActionRow):
    """
    A preferences row with a title and a file chooser button
    title: the title shown
    file_chooser_title: the title of the file chooser dialog
    conf_key: the key of the configuration dictionary/json in ConfManager
    signal: an optional signal to let ConfManager emit when the value changes
    """

    def __init__(self, title, conf_key, signal=None,
                 file_chooser_title=None,
                 subtitle=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        if subtitle:
            self.subtitle = subtitle
            self.set_subtitle(self.subtitle)
        self.confman = ConfManager()
        self.set_title(self.title)
        self.signal = signal
        self.conf_key = conf_key

        self.file_chooser_btn = Gtk.FileChooserButton.new(
            file_chooser_title or _('Choose a folder'),
            Gtk.FileChooserAction.SELECT_FOLDER
        )
        self.file_chooser_btn.set_current_folder_uri(
            'file://'+self.confman.conf[self.conf_key]
        )

        self.file_chooser_btn.connect('file-set', self.on_file_set)
        self.add(self.file_chooser_btn)

    def on_file_set(self, *args):
        self.confman.conf[self.conf_key] = self.file_chooser_btn.get_filename()
        if self.signal:
            self.confman.emit(self.signal, '')
        self.confman.save_conf()


class PreferencesSpinButtonRow(Handy.ActionRow):
    """
    A preferences row with a title and a spin button
    title: the title shown
    min_v: minimum num value
    max_v: maximum num value
    conf_key: the key of the configuration dictionary/json in ConfManager
    signal: an optional signal to let ConfManager emit when the value changes
    """

    def __init__(self, title, min_v, max_v, conf_key, signal=None,
                 subtitle=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        if subtitle:
            self.subtitle = subtitle
            self.set_subtitle(self.subtitle)
        self.confman = ConfManager()
        self.set_title(self.title)
        self.signal = signal
        self.conf_key = conf_key

        self.adjustment = Gtk.Adjustment(
            self.confman.conf[self.conf_key],  # initial value
            min_v,  # minimum value
            max_v,  # maximum value
            1,  # step increment
            7,  # page increment (page up, page down? large steps anyway)
            0
        )

        self.spin_button = Gtk.SpinButton()
        self.spin_button.set_adjustment(self.adjustment)
        self.spin_button.set_valign(Gtk.Align.CENTER)
        self.spin_button.connect('value-changed', self.on_value_changed)
        self.add(self.spin_button)
        # You need to interact with the actual spin button
        # Avoids accidental presses
        # self.set_activatable_widget(self.button)

    def on_value_changed(self, *args):
        self.confman.conf[self.conf_key] = self.spin_button.get_value_as_int()
        if self.signal:
            self.confman.emit(self.signal, self.confman.conf[self.conf_key])
        self.confman.save_conf()


class PreferencesComboBoxRow(Handy.ActionRow):
    """
    A preferences row with a title and a combo box
    title: the title shown
    values: a list of acceptable values
    values_names: a list of user facing names for the values provided above
    conf_key: the key of the configuration dictionary/json in ConfManager
    signal: an optional signal to let ConfManager emit when the value changes
    """

    def __init__(self, title, values, values_names, conf_key, signal=None,
                 subtitle=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        if subtitle:
            self.subtitle = subtitle
            self.set_subtitle(self.subtitle)
        self.confman = ConfManager()
        self.set_title(self.title)
        self.signal = signal
        self.conf_key = conf_key
        self.list_store = Gtk.ListStore(str, str)
        for name, value in zip(values_names, values):
            self.list_store.append([value, name])
        self.combo_box = Gtk.ComboBox.new_with_model(self.list_store)
        self.cell_renderer = Gtk.CellRendererText()
        self.combo_box.pack_start(self.cell_renderer, True)
        self.combo_box.add_attribute(self.cell_renderer, "text", 1)
        self.combo_box.set_id_column(0)
        self.combo_box.set_active_id(self.confman.conf[self.conf_key])
        self.add(self.combo_box)
        self.combo_box.connect('changed', self.on_value_changed)

    def on_value_changed(self, *args):
        store_iter = self.combo_box.get_active_iter()
        if store_iter is not None:
            self.confman.conf[self.conf_key] = \
                self.combo_box.get_model()[store_iter][0]
            if self.signal:
                self.confman.emit(self.signal, '')
            self.confman.save_conf()


class PreferencesToggleRow(Handy.ActionRow):
    """
    A preferences row with a title and a toggle
    title: the title shown
    conf_key: the key of the configuration dictionary/json in ConfManager
    signal: an optional signal to let ConfManager emit when the configuration
        is set
    """
    def __init__(self, title, conf_key, signal=None,
                 subtitle=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        if subtitle:
            self.subtitle = subtitle
            self.set_subtitle(self.subtitle)
        self.confman = ConfManager()
        self.set_title(self.title)
        self.conf_key = conf_key
        self.signal = signal

        self.toggle = Gtk.Switch()
        self.toggle.set_valign(Gtk.Align.CENTER)
        if self.conf_key == 'selection_mode':
            self.toggle.set_active(
                self.confman.conf[self.conf_key] == 'double'
            )
        else:
            self.toggle.set_active(self.confman.conf[self.conf_key])
        self.toggle.connect('state-set', self.on_toggle_state_set)
        self.add(self.toggle)
        self.set_activatable_widget(self.toggle)

    def on_toggle_state_set(self, toggle, state):
        self.confman.conf[self.conf_key] = state
        self.confman.save_conf()
        if self.signal:
            self.confman.emit(self.signal, '')


class GeneralPreferencesPage(Handy.PreferencesPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(_('General'))
        self.set_icon_name('preferences-other-symbolic')

        self.general_preferences_group = Handy.PreferencesGroup()
        self.general_preferences_group.set_title(_('General Settings'))
        toggle_settings = [
        ]
        for s in toggle_settings:
            row = PreferencesToggleRow(
                s['title'],
                s['conf_key'],
                s['signal'],
                s['subtitle'] if 'subtitle' in s.keys() else None
            )
            self.general_preferences_group.add(row)
        # self.general_preferences_group.add(
        #     PreferencesFileChooserRow(
        #         _('Notes folder'),
        #         'notes_dir',
        #         signal='notes_dir_changed',
        #         file_chooser_title=_('Choose a notes folder')
        #     )
        # )
        # self.general_preferences_group.add(
        #     PreferencesComboBoxRow(
        #         _('Sort notes by'),
        #         ['name', 'last_modified'],
        #         [_('Name'), _('Last modified')],
        #         'sorting_method',
        #         signal='sorting_method_changed'
        #     )
        # )
        self.add(self.general_preferences_group)
        self.show_all()


class ViewPreferencesPage(Handy.PreferencesPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(_('View'))
        self.set_icon_name('applications-graphics-symbolic')

        self.view_preferences_group = Handy.PreferencesGroup()
        self.view_preferences_group.set_title(_('View Settings'))
        toggle_settings = [
            {
                'title': _('Dark mode'),
                'conf_key': 'dark_mode',
                'signal': 'dark_mode_changed'
            },
        ]
        for s in toggle_settings:
            row = PreferencesToggleRow(s['title'], s['conf_key'], s['signal'])
            self.view_preferences_group.add(row)
        self.add(self.view_preferences_group)

        # self.view_preferences_group.add(
        #     PreferencesComboBoxRow(
        #         _('Editor color scheme'),
        #         color_schemes,
        #         [
        #             c.capitalize() if c != 'default' else _('Default')
        #             for c in color_schemes
        #         ],
        #         'editor_color_scheme',
        #         'editor_color_scheme_changed'
        #     )
        # )
        # self.view_preferences_group.add(
        #     PreferencesSpinButtonRow(
        #         _('Font size'),
        #         1,
        #         300,
        #         'font_size',
        #         signal='font_size_changed'
        #     )
        # )

        self.show_all()


class SettingsWindow(Handy.PreferencesWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confman = ConfManager()

        self.pages = [
            # GeneralPreferencesPage(),
            ViewPreferencesPage()
        ]
        for p in self.pages:
            self.add(p)
        self.set_default_size(630, 700)
        # self.get_titlebar().set_show_close_button(True)

        self.accel_group = Gtk.AccelGroup()
        self.accel_group.connect(
            *Gtk.accelerator_parse('Escape'), Gtk.AccelFlags.VISIBLE,
            lambda *args: self.close()
        )
        self.add_accel_group(self.accel_group)
