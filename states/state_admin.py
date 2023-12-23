from aiogram.dispatcher.filters.state import State, StatesGroup


class ReklamaState(StatesGroup):
    rek = State()


class AddMedia(StatesGroup):
    media = State()
    media_id = State()


class AddChannelState(StatesGroup):
    username = State()
    channel_id = State()


class DeleteChannelState(StatesGroup):
    username = State()


class DeleteMovieState(StatesGroup):
    post_id = State()
    