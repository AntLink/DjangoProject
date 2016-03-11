def load_general_setting_stores(apps, schema_editor):
    Setting = apps.get_model("setting", "Setting")
    site_title = Setting(
        name='Site Title',
        value='site_title',
        content='AntLink',
        type='general',
        autoload='yes'
    )
    site_title.save()

    tag_line = Setting(
        name='Tag Line',
        value='tag_line',
        content='AntLink Project',
        type='general',
        autoload='yes'
    )
    tag_line.save()

    site_language = Setting(
        name='Site Language',
        value='site_language',
        content='id',
        type='general',
        autoload='yes'
    )
    site_language.save()

    email = Setting(
        name='Email Address',
        value='email_address',
        content='example@gmail.com',
        type='general',
        autoload='yes'
    )
    email.save()

    timezone = Setting(
        name='Timezone',
        value='timezon',
        content='timezon json format',
        type='general',
        autoload='yes'
    )
    timezone.save()

    date_format = Setting(
        name='Date Format',
        value='date_format',
        content='date format json format',
        type='general',
        autoload='yes'
    )
    date_format.save()

    site_keyword = Setting(
        name='Site Keyword',
        value='site_keyword',
        content='AntLink Meta Keyword',
        type='general',
        autoload='yes'
    )
    site_keyword.save()

    site_author = Setting(
        name='Author',
        value='site_author',
        content='Site Author',
        type='general',
        autoload='yes'
    )
    site_author.save()

    site_description = Setting(
        name='Description',
        value='site_description',
        content='Site Description',
        type='general',
        autoload='yes'
    )
    site_description.save()

    admin_colpase_menu = Setting(
        name='Colpase Menu',
        value='admin_colpase_menu',
        content='mainnav-lg',
        type='admin',
        autoload='yes'
    )
    admin_colpase_menu.save()

    admin_navbar_fixed = Setting(
        name='Navbar Fixed',
        value='admin_navbar_fixed',
        content='navbar-fixed',
        type='admin',
        autoload='yes'
    )
    admin_navbar_fixed.save()

    admin_mainnav_fixed = Setting(
        name='Main Nav Fixed',
        value='admin_mainnav_fixed',
        content='mainnav-fixed',
        type='admin',
        autoload='yes'
    )
    admin_mainnav_fixed.save()


def load_reading_setting_stores():
    pass
