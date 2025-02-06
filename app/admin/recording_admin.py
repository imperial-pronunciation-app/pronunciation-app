from sqladmin import ModelView

from app.models import Recording


class RecordingAdmin(ModelView, model=Recording): # type: ignore[call-arg]
    column_list = [Recording.id, Recording.recording_s3_key, Recording.user_id, Recording.word_id, Recording.created_at]
    column_sortable_list = [Recording.id, Recording.recording_s3_key, Recording.user_id, Recording.word_id, Recording.created_at]
