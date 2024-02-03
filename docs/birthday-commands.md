# Birthday Commands

This bot allows remembering birthdays as well as posting messsages as reminders of baby month milestones (ex. `1 month`, `2 months`, etc).

## Admin Commands

These commands are only availabl

- `/birthday-admin settings`: Set the `birthday_channel` and the `baby_month_milestone_channel`. Without these two channels set, birthday and baby month milestone messages will not post.
- `/birthday-admin add`: Add a birthday with a name, date, and user. Date must be added in the `MM/DD/YYYY` format. Names must be unique per user.
- `/birthday-admin remove`: Remove a birthday assigned to a specific user by `name`.

## Regular Commands

- `/birthday add`: Add a birthday with a name and a date. Date must be added in the `MM/DD/YYYY` format. Names must be unique per user.
- `/birthday remove`: Remove a birthday assigned to your user by `name`.
- `/birthday list`: Given a `user`, list all birthdays assigned to that user.
- `/birthday upcoming`: Gives a list of birthdays in the next month
