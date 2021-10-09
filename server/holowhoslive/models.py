from tortoise import fields, models


class Group(models.Model):
    name = fields.CharField(max_length=255)
    platform = fields.CharField(max_length=255)

    class PydanticMeta:
        exclude = ["yt_channels", "twitch_channels"]


class YtChannel(models.Model):
    last_name = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255)
    channel_id = fields.CharField(max_length=255)

    group = fields.ForeignKeyField("models.Group", related_name="yt_channels")


class TwitchChannel(models.Model):
    last_name = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255)
    channel_id = fields.CharField(max_length=255)

    group = fields.ForeignKeyField("models.Group", related_name="twitch_channels")
