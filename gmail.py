import asyncio
from pyppeteer import launch, connect
import json
import traceback
import requests
import os
import random
from smsactivate.api import SMSActivateAPI
from datetime import datetime


SMS_KEY = ''
PROXY = ''
HOSTInco = 'http://127.0.0.1:35000'

smsAPI = SMSActivateAPI(SMS_KEY)


def change_proxy():
    requests.get('https://mobileproxy.space/reload.html?proxy_key=')
    return



async def open_browser(url):
    browser = await connect(browserURL = url, ignoreHTTPSErrors = True)
    await asyncio.sleep(3)
    page = list(await browser.pages())[0]
    await page.setViewport({'width': 800, 'height': 600})
    return page, browser



""" Прогреваем профиль браузера """
async def warmingUpProfile(page):

    """ Получаем гео прокси """
    await gotoUrl(page, 'https://www.reg.ru/web-tools/geoip')
    await page.waitForSelector('#ip_input')
    city = await page.J('#b-ip-info__city')
    city = await page.evaluate('city => city.innerText', city)
    await page.waitFor(random.randrange(3000, 6000))


    for text in [f'{city} погода на неделю', f'{city} купить квартиру']:
        """ Переходим в гугл """
        await gotoUrl(page, 'https://www.google.com/')
        await page.waitFor(random.randrange(3000, 5000))


        """ Забиваем поисковый запрос + гео """
        [[await page.type('input[class="gLFyf gsfi"]', i), await page.waitFor(random.randrange(100, 200))] for i in text]
        await page.keyboard.press('Enter')
        await page.waitFor(random.randrange(5000, 8000))

        """ Кликаем по выдаче """
        elemnt = await page.J('div.NJo7tc.Z26q7c.jGGQ5e > div > a > h3')
        await elemnt.click()
        await page.waitFor(random.randrange(3000, 6000))

        """ Имитируем действия на странице """
        for i in range(5):
            await page.keyboard.press(random.choice(['End', 'Home']))
            await page.waitFor(random.randrange(2000, 5000))

        await page.waitFor(random.randrange(3000, 6000))


    return

async def gotoUrl(page, url):
    count = 0
    while True:
        try:
            await page.goto(url)
            break
        except:
            pass
        count += 1
        if count >= 5:
            break

    return

""" Закрыть и удалить профиль """
async def closeAndDelete(key):
    requests.get(f'{HOSTInco}/profile/stop/{key}')
    await asyncio.sleep(3)
    requests.get(f'{HOSTInco}/profile/delete/{key}')
    return


dicKey = {'Ь':'', 'ь':'', 'Ъ':'', 'ъ':'', 'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
       'Г':'G', 'г':'g', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e', 'Ё':'Yo', 'ё':'yo', 'Ж':'Zh', 'ж':'zh',
       'З':'Z', 'з':'z', 'И':'I', 'и':'i', 'Й':'Y', 'й':'y', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
       'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r', 
       'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'H', 'х':'h',
       'Ц':'Ts', 'ц':'ts', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Sch', 'щ':'sch', 'Ы':'Yi',
       'ы':'yi', 'Э':'E', 'э':'e', 'Ю':'Yu', 'ю':'yu', 'Я':'Ya', 'я':'ya', ' ': '.'}

""" Регистрация mail """
async def registerGMail(page):
    with open('FIO.txt', 'r', encoding = 'utf-8') as f:
        fio = f.read().split('\n')

    fio = random.choice(fio)
    _name = fio.split(' ')[0]
    _sname = fio.split(' ')[1]
    _mail = ''.join([dicKey[i] for i in fio])
    _mail = _mail+'.'+str(random.randrange(10000, 100000))
    _mail = _mail.lower()

    _password = ''
    for x in range(12): 
        _password = _password + random.choice(list('!#%$&1234567890abcdefghigklmnopqrstuvyxwz!#%$&ABCDEFGHIGKLMNOPQRSTUVYXWZ!#%$&'))

    with open('mailAccs.txt', 'r') as f:
        MAIL = f.read().split('\n')
        listMAIL = [i for i in MAIL if i != ""]

    MAIL = random.choice(listMAIL)
    
    saveMAIL = [i for i in listMAIL if i != MAIL]
    with open('mailAccs.txt', 'w') as f:
        f.write('\n'.join(saveMAIL))


    extra_mail = MAIL.split(':')[0]
    extra_mail_pass = MAIL.split(':')[1]

    await gotoUrl(page, 'https://accounts.google.com/signup')

    
    await page.waitForSelector('#firstName')

    """ Имя """
    [[await page.type('#firstName', i), await page.waitFor(100)] for i in _name]
    
    """ Фамилия """
    [[await page.type('#lastName', i), await page.waitFor(100)] for i in _sname]

    """ Gmail """
    [[await page.type('#username', i), await page.waitFor(100)] for i in _mail]

    """ Пароль """
    for pswd in await page.JJ('input[type="password"]'):
        [[await pswd.type(i), await page.waitFor(100)] for i in _password]


    await page.click('#accountDetailsNext')
    await page.waitFor(5000)
    check = await verifyAccount(page, extra_mail)
    if check:
        now = datetime.now()
        date = f'{now.year}-{now.month}-{now.day}'


        with open(f'accounts.txt', 'a', encoding = 'utf-8') as f:
            f.write(f'{_mail}@gmail.com:{_password}:{extra_mail}:{extra_mail_pass}\n')

        with open(f'{date}.txt', 'a+', encoding = 'utf-8') as f:
            f.write(f'{_mail}@gmail.com:{_password}:{extra_mail}:{extra_mail_pass}\n')

        return True

    return False


async def verifyAccount(page, extra_mail):
    await page.waitForSelector('#phoneNumberId')

    while True:
        while True:
            number_phone = smsAPI.getNumber(service='go', country = 0)
            try:
                smsID = number_phone['order_id']
                number_phone = number_phone['phone']
                break
            except:
                await asyncio.sleep(5)
                
        await page.waitFor(3000)
        [[await page.type('#phoneNumberId', i), await page.waitFor(100)] for i in str(number_phone)]

        await page.waitFor(1000)
        await page.click('button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b"]')
        await page.waitFor(5000)

        if await page.JJ('span[class="jibhHc"]'):
            """ Номер уже используется """
            smsAPI.setStatus(id = smsID, status = 8)

            clear = await page.J('#phoneNumberId')
            await clear.click()
            await page.keyboard.down('Control')
            await page.keyboard.press('KeyA')
            await page.keyboard.up('Control')
            await page.keyboard.press('Backspace')
            await page.waitFor(1500)

        else:
            break


    """ Смс отправлено """
    smsAPI.setStatus(id = smsID,status = 1)

    while True:
        status = smsAPI.getStatus(id = smsID)
        try:
            stat = smsAPI.activationStatus(status)
            if 'STATUS_OK' in stat['status']:
                code = stat['status'].split(':')[1].strip()
                break
        except:
            code = False
            await asyncio.sleep(5)


    """ Подтвердит смс """
    smsAPI.setStatus(id = smsID,status = 6)

    if code:
        await page.type('#code', code)
        await page.waitFor(1000)
        await page.click('button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b"]')

        await page.waitForSelector('input[type="email"]')
        await page.waitFor(3000)

        """ Резервная почта """
        [[await page.type('input[type="email"]', i), await page.waitFor(100)] for i in str(extra_mail)]

        """ День рождения """
        await page.type('input[id="day"]', str(random.randrange(1, 25)))
        await page.waitFor(1000)

        """ Год рождения """
        await page.type('input[id="year"]', str(random.randrange(1980, 2000)))
        await page.waitFor(1000)

        """ Выбрать пол"""
        await page.select('select[id="gender"]', '2')
        await page.select('select[id="month"]', str(random.randrange(1, 11)))

        """ Далее """
        await page.click('button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b"]')
        await page.waitFor(5000)

        """ Пропустить """
        await page.waitForSelector('div[class="daaWTb"]', timeout = 60000)
        await page.click('div[class="daaWTb"]')
        await page.waitFor(5000)

        """ Completed """
        await page.waitForSelector('button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b"]', timeout = 60000)
        await page.click('button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b"]')

        await page.waitFor(10000)
        return True

    return False




async def main(key, url):
    page, browser = await open_browser(url)
    if not page: return 'Browser not found'
    await asyncio.sleep(10000)
    try:
        await warmingUpProfile(page)
    except:
        pass

    answer = await registerGMail(page)
    await closeAndDelete(key)
    if answer:
        return 'Create new account'
    return 'Error create account'





def getBrowserUrl(key):
    errors = 0
    while True:
        try:
            requests.get(f'{HOSTInco}/profile/stop/{key}', timeout=5)
            data = requests.get(f"{HOSTInco}/automation/launch/puppeteer/{key}")
            data = json.loads(data.text)
        except Exception as err:
            errors += 1
            if errors >= 5:
                requests.get(f'{HOSTInco}/profile/stop/{key}', timeout=5)
                return False
            continue

        if 'puppeteerUrl' in data and 'successes' in data:
            url = data['puppeteerUrl']
            break   
        else:
            return False


    return url

""" Создать профиль """
def createProfile():

    host = PROXY.split('@')[0].strip()
    plogin = PROXY.split('@')[1].split(":")[0].strip()
    ppassword = PROXY.split('@')[1].split(":")[1].strip()
    general = {"general_profile_information": 
                    {"profile_name": f"Proxy",
                    "profile_notes": "",
                    "simulated_operating_system": "Windows"},

                'Proxy': {"connection_type": "Socks 5 proxy",
                    "proxy_url": host,
                    "proxy_username": plogin,
                    "proxy_password": ppassword,
                    "proxy_rotating": "0"}}



    general = json.dumps(general)

    data = {"profileData" : str(general)}

    r = requests.post(f'{HOSTInco}/profile/add', data = data)
    key = json.loads(r.text)
    if 'profile_browser_id' in key: 
        key = key['profile_browser_id']
        return key

    else:
        return False


if __name__ == '__main__':
    while True:
        balance = smsAPI.getBalance()
        if float(balance['balance']) <= 10:
            print('Кончились деньги на смске')
            break

        change_proxy()
        key = createProfile()
        if key:
            url = getBrowserUrl(key)
            if url:
                print(asyncio.run(main(key, url), debug = False))
            else:
                print('Not url browser')

        else:
            print('Not key incogniton')






