from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from loader import bot, db
import random
from aiogram.utils.markdown import hitalic, hbold
class Question:
    def __init__(self, text, answers):
        self.text = text
        self.answers = answers

class Quiz:
    def __init__(self, questions):
        self.original_questions = list(questions)
        self.questions = []
        self.scores = {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}
        self.current_question = 0
        self.is_started = False

    async def start(self, message):
        if not self.is_started:
            self.is_started = True
            self.questions = list(self.original_questions)
            self.scores = {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}  # scores ni nolga qaytaring
            self.current_question = 0  # current_question ni nolga qaytaring
            random.shuffle(self.questions)
            question = self.questions[self.current_question]
            buttons = []
            for i, answer in enumerate(question.answers):
                callback_data = f"answer_{i}"
                inline_btn = types.InlineKeyboardButton(text=answer['text'], callback_data=callback_data)
                buttons.append([inline_btn])
            inline_kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            await bot.send_message(message.chat.id, question.text, reply_markup=inline_kb)

    async def next_question(self, query, answer_index):
        answer = self.questions[self.current_question].answers[answer_index]
        for house, score in answer['scores'].items():
            self.scores[house] += score
        self.questions.pop(self.current_question)
        if self.questions:
            random.shuffle(self.questions)
            question = self.questions[self.current_question]
            buttons = []
            for i, answer in enumerate(question.answers):
                callback_data = f"answer_{i}"
                inline_btn = types.InlineKeyboardButton(text=answer['text'], callback_data=callback_data)
                buttons.append([inline_btn])
            inline_kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
            await bot.send_message(query.message.chat.id, question.text, reply_markup=inline_kb)
        else:
            result = max(self.scores, key=self.scores.get)
            if result == 'Grifindor':
                await bot.send_photo(chat_id= query.message.chat.id, photo="AgACAgIAAxkBAAICp2VY31shcY3JOFPGSop-HsUpMhxGAALZ0zEbwlXJSnpgMD-tSgABwgEAAwIAA3gAAzME", caption=hbold("Siz o'z fakultetingizni topdingiz"))
            elif result == 'Hufflepuff':
                await bot.send_photo(chat_id= query.message.chat.id, photo="AgACAgIAAxkBAAICq2VY32gxSwLScbdr1ixskhYJBX3BAALb0zEbwlXJSqcY4o4XntHNAQADAgADeAADMwQ", caption=hbold("Siz o'z fakultetingizni topdingiz"))
            elif result == 'Ravenclaw':
                await bot.send_photo(chat_id= query.message.chat.id, photo="AgACAgIAAxkBAAICqWVY311fnlvRUQs9VPuUWnicfOzrAALa0zEbwlXJSkPimNzpcsFaAQADAgADeAADMwQ", caption=hbold("Siz o'z fakultetingizni topdingiz"))
            elif result == 'Slytherin':
                 await bot.send_photo(chat_id= query.message.chat.id, photo="AgACAgIAAxkBAAICpWVY3tD5fySI3m9m1GZTSPjP0JjBAALX0zEbwlXJSp7eavvu_9MKAQADAgADeAADMwQ", caption=hbold("Siz o'z fakultetingizni topdingiz"))
            
            text = f"Qara do'stim  bu  mening fakultetim  {result}. Kel, sen ham o'z fakultetingni aniqlab olasan )  bu yerga bos o'rtoq:\n\n https://t.me/donishmand_hatbot "
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text="Do'stlarga bildiring", url=f"https://t.me/share/url?url={text}")
                    ]
                ]
            )
            await bot.send_message(query.message.chat.id, text, reply_markup=keyboard)
            db.update_user_facultet(query.from_user.id, result)
            self.is_started = False

questions = [
    Question(
        "Oy yoki yulduzlar?",
        [
            {"text": "Oy", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 50, "Slytherin": 50}},
            {"text": "Yulduzlar", "scores": {"Grifindor": 30, "Hufflepuff": 50, "Ravenclaw": 10, "Slytherin": 10}},
        ],
    ),   
    Question(
        "Odamlar sizni nima desa jaxlingiz chiqadi?",
        [
            {"text": "Oddiy", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
            {"text": "Bilimsiz", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Qoʻrqoq", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Xudbin", "scores": {"Grifindor": 0, "Hufflepuff": 100, "Ravenclaw": 0, "Slytherin": 0}},
        ],
    ),
    Question(
        "O'lganingizdan keyin odamlar sizni nima deyishini eshitib xursand boʻlardingiz? ",
        [
            {"text": "Sogʻinadi, lekin jilmayadi", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Sizning sarguzashtlaringiz haqida kop soʻraydi", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Sizning yutuqlaringiz haqida oʻylaydi", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Menga oʻlganimdan keyin nima deb oʻylashlari qiziqmas, menga men tirikligimda nima deb oʻylashlari qiziq", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
        ],
    ),
    Question(
        "Tarixda qanday nom bilan qolishni xohlaysiz? ",
        [
            {"text": "Daho", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Yaxshi", "scores": {"Grifindor": 0, "Hufflepuff": 100, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Zoʻr", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
            {"text": "Jasur", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
        ],
    ),
    Question(
        "Imkon berilganda qanday eliksir yaratardingiz?  ",
        [
            {"text": "Sevgi", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Shon-sharaf ", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Donolik", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Kuch", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
        ],
    ),
    Question(
        "Flutterby butasi har asrda bir marta xushboʻy hidli gul chiqaradi. Agar u sizni oʻziga jalb qilsa qanaqa hidli boʻlardi?  ",
        [
            {"text": "Yogʻoch olov", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Dengiz ", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
            {"text": "Yangi pergament", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Uy", "scores": {"Grifindor": 0, "Hufflepuff": 100, "Ravenclaw": 0, "Slytherin": 0}},
        ],
    ),
    Question(
        "4 ta goblin sizdan oldin joylashishdi. Qaysi birini ichishni tanlardingiz?  ",
        [
            {"text": "Ko'pikli, ichida maydalangan olmos bordek yaltirab turgan suyuqlik", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Shokoladning mazzali hidi keladigan silliq qalin binafsha rang ichimlik ", "scores": {"Grifindor": 0, "Hufflepuff": 100, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Tilla rang ko'zni yaralaydigan yorqin suyuqlik u butun xona boʻylab quyosh soyalari raqsini ijro etadi", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Sirli qora siyohdek portlaydigan g'alati tassavurlarni keltirib chiqaradigan suyuqlik", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
        ],
    ),
    Question(
        "Qaysi cholgʻu asbobi qulogʻiningizga yoqimli eshitiladi",
        [
            {"text": "Skripka", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
            {"text": "Karnaylar", "scores": {"Grifindor": 0, "Hufflepuff": 100, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Pianino", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Baraban", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
        ],
    ),
    Question(
        "Siz sexrlangan bog'ga kirdingiz birinchi nimani sinashga shoshardingiz? ",
        [
            {"text": "Tilla olma beradigan kumush bargli daraxt", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 100, "Slytherin": 0}},
            {"text": "Bir biri bilan gaplashayotgandek koʻrinadigan semiz qizil qo'ziqorin", "scores": {"Grifindor": 0, "Hufflepuff": 100, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Chuqurida nur aylanayotgan ko'pikli hovuz", "scores": {"Grifindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 100}},
            {"text": "Koʻzi miltillab turgan qari sehrgar haykali", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
        ],
    ),
    Question(
        "4 ta quti oldingizda joylashgan . Qaysi birini ochishga harakat qilardingiz? ",
        [
            {"text": "Oltin bilan bezatilgan kichik toshbaqa qutisi. Ichidagi mavjudotlar chiyillab turganga oʻxshaydi. ", "scores": {"Grifindor": 50, "Hufflepuff": 50, "Ravenclaw": 0, "Slytherin": 0}},
            {"text": "Qora yaltiroq kumush qulf va kaliti bor, sirli Run yozuvida Merlin deb yozilgan quti", "scores": {"Grifindor": 50, "Hufflepuff":0, "Ravenclaw": 0, "Slytherin": 50}},
            {"text": "Tirnoqli oyoqlarda turgan bezatilgan oltin quti unga bilim va chidab boʻlmas vasvasaga duchor boʻlish haqida ogohlantirilgan", "scores": {"Grifindor": 60, "Hufflepuff": 0, "Ravenclaw": 50, "Slytherin": 100}},
            {"text": "Kichkina qalay qutisi ustida men faqat munosiblar uchun ochilaman degan xabar bor", "scores": {"Grifindor": 100, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}},
        ],
    ),
]

quiz = Quiz(questions)

menu_router: Router = Router()

@menu_router.callback_query(F.data =="facultcheck")
async def menu(query: CallbackQuery):
    user = db.select_user(id=query.from_user.id)
    
    if user:
        keyboard = types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                             types.InlineKeyboardButton(text="Ha", callback_data="update_facultet"),
                          types.InlineKeyboardButton(text="Yo'q", callback_data="no_update"),
                        ]
                    ]
                    
                    )
       
      
        await bot.send_message(query.message.chat.id, f"Sizning fakultet: { user[2] if user[2] else 'Fakultet topilmadi'}. Fakultetni yangilamoqchimisiz?", reply_markup=keyboard)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    else:
        await quiz.start(query.message)
    
@menu_router.callback_query(F.data =="update_facultet")
async def update_facultet(query: CallbackQuery):
    await bot.send_message(query.message.chat.id, "Fakultetni yangilashni boshladik.")
    await quiz.start(query.message)
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
@menu_router.callback_query(F.data =="no_update")
async def no_update(query: CallbackQuery):
    user = db.select_user(id=query.from_user.id)
    if user:
        facultet = user[2]
        count = db.count_facultet_members(facultet)
        await bot.send_message(query.message.chat.id, f"Ajoyib! \n\nSiz haliyam biz bilansiz. Sizning fakultetingizda {count} ta a'zo bor.")
        text = f"Qaragin bu  mening fakultetim  {facultet}. Kel, sen ham o'z fakultetingni aniqlab olasan )  bu yerga bos o'rtoq:\n\n https://t.me/donishmand_hatbot "
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Do'stlarga bildiring", url=f"https://t.me/share/url?url={text}")
                ]
            ]
        )
        await bot.send_message(query.message.chat.id, text, reply_markup=keyboard)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    else:
        await quiz.start(query.message)

@menu_router.callback_query(lambda c: c.data and c.data.startswith('answer_'))
async def process_callback_kb1btn1(callback_query: CallbackQuery):
    if quiz.is_started:
        answer_index = int(callback_query.data.split('_')[1])
        await quiz.next_question(callback_query, answer_index)

@menu_router.callback_query(F.data == 'admincall')
async def admincall(callback_query: CallbackQuery):
    await bot.send_message(callback_query.message.chat.id, "https://t.me/husniddin1213")
@menu_router.callback_query(F.data == 'info')
async def admincall(callback_query: CallbackQuery):
    await bot.send_message(callback_query.message.chat.id, f"Assalomu alaykum {callback_query.from_user.full_name}  \n\n1. Agar sizda savollar yuzasidan savol bo'lsa murojaat qiling. Tog'rilaymiz. \n2. Botga qanday hususiyatlar qo'shsak yaxshi? Bizga ayting.\n3. Botda xatolik bormi? Bizda ayting to'girlaymiz. \n\n Pottermanlar birgalikda kuchli  \n\n\n {hitalic('Botdagi savollar http://wizardmore.com/ saytiga tegishli. Tarjimada xatoliklar uchrashi mumkin. Ushbu saytlar orqali yana yaxshiroq savollar olishingiz mumkin - http://wizardmore.com/sorting-hat/   https://www.wizardingworld.com/ ')} ")