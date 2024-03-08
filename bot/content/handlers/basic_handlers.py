import logging
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import models, db
from .keyboards import kb, ikb

import bot.content.states as st


router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext, database: db.Database) -> None:
    current_state = await state.get_state()
    await msg.answer(f"Hi, Im started! Current state is {current_state}")


# States can be set:
# async def set_state(msg: types.Message, state: FSMContext) -> None:
#     await state.set_state(st.SomeState.state1)
