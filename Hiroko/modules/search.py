from traceback import format_exc
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.myanimelist import Search as AnimeSearch
from search_engine_parser.core.engines.stackoverflow import \
    Search as StackSearch
from search_engine_parser.core.exceptions import NoResultsFound, NoResultsOrTrafficError
from Hiroko import Hiroko
from pyrogram import filters




gsearch = GoogleSearch()
anisearch = AnimeSearch()
stsearch = StackSearch()



def ikb(rows=None, back=False, todo="start_back"):
    """
    rows = pass the rows
    back - if want to make back button
    todo - callback data of back button
    """
    if rows is None:
        rows = []
    lines = []
    try:
        for row in rows:
            line = []
            for button in row:
                btn_text = button.split(".")[1].capitalize()
                button = btn(btn_text, button)  # InlineKeyboardButton
                line.append(button)
            lines.append(line)
    except AttributeError:
        for row in rows:
            line = []
            for button in row:
                button = btn(*button)  # Will make the kb which don't have "." in them
                line.append(button)
            lines.append(line)
    except TypeError:
        # make a code to handel that error
        line = []
        for button in rows:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    if back: 
        back_btn = [(btn("« Back", todo))]
        lines.append(back_btn)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def btn(text, value, type="callback_data"):
    return InlineKeyboardButton(text, **{type: value})






@Hiroko.on_message(command('google'))
async def g_search(c: Hiroko, m: Message):
    split = m.text.split(None, 1)
    if len(split) == 1:
        return await m.reply_text("No query given\nDo `/help search` to see how to use it")
    to_del = await m.reply_text("Searching google...")
    query = split[1]
    try:
        result = await gsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"Here are the results of requested query **{query.upper()}**"
        await to_del.delete()
        await m.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await m.reply_text("No result found corresponding to your query")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await m.reply_text("No result found due to too many traffic")
        return
    except Exception as e:
        await to_del.delete()
        await m.reply_text(f"Got an error:\nReport it at @DevsOops")
        print(f"error : {e}")
        return



@Hiroko.on_message(command('anime'))
async def anime_search(c: Hiroko, m: Message):
    split = m.text.split(None, 1)
    if len(split) == 1:
        return await m.reply_text("No query given\nDo `/help search` to see how to use it")
    to_del = await m.reply_text("Searching myanimelist...")
    query = split[1]
    try:
        result = await anisearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"Here are the results of requested query **{query.upper()}**"
        await to_del.delete()
        await m.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await m.reply_text("No result found corresponding to your query")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await m.reply_text("No result found due to too many traffic")
        return
    except Exception as e:
        await to_del.delete()
        await m.reply_text(f"Got an error:\nReport it at @DevsOops")
        print(f"error : {e}")
        return


@Hiroko.on_message(command('stack'))
async def stack_search(c: Hiroko, m: Message):
    split = m.text.split(None, 1)
    if len(split) == 1:
        return await m.reply_text("No query given\nDo `/help search` to see how to use it")
    to_del = await m.reply_text("Searching Stackoverflow...")
    query = split[1]
    try:
        result = await stsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"Here are the results of requested query **{query.upper()}**"
        await to_del.delete()
        await m.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await m.reply_text("No result found corresponding to your query")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await m.reply_text("No result found due to too many traffic")
        return
    except Exception as e:
        await to_del.delete()
        await m.reply_text(f"Got an error:\nReport it at @DevsOops")
        print(f"error : {e}")
        return





