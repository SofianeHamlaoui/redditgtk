# How to create and update a translation

First, run the script `update_potfiles.sh` like this, where `LANGUAGE` is the language code that you want to add or update (`it`: italian, `fr`: french, `es`: spanish...):

```bash
cd po
./update_potfiles.sh LANGUAGE
```

It will ask for an email, provide yours if you want and it will be used to credit you. It's historically been used to report issues in the translation for a specific language, but nowadays with issue systems and easier bug reporting than ever it's not really necessary.

Finally edit the `.po` file that was just created with the language code you used. You can use a normal text editor or a simpler tool like **lokalize** or **poedit** (you can probably find both in your distribution's repositories).

If you need any help, feel free to open an issue.
