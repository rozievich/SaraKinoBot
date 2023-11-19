from aiogram.dispatcher.filters.state import State, StatesGroup


class ReklamaState(StatesGroup):
    rek = State()


class AddMedia(StatesGroup):
    media = State()


class AddChannelState(StatesGroup):
    username = State()


class DeleteChannelState(StatesGroup):
    username = State()
