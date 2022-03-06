import asyncio
from pyppeteer import launch, connect
import json
import traceback
import requests
import os
import random
from rucaptcha import RuCaptchaConnection 
from smsactivate.api import SMSActivateAPI






RUCAPTCHA_KEY = ''
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
    await page.setViewport({'width': 1920, 'height': 1080})
    return page, browser



""" Прогреваем профиль браузера """
async def warmingUpProfile(page):

    """ Получаем гео прокси """
    await page.goto('https://www.reg.ru/web-tools/geoip')
    await page.waitForSelector('#ip_input')
    city = await page.J('#b-ip-info__city')
    city = await page.evaluate('city => city.innerText', city)
    await page.waitFor(random.randrange(3000, 6000))


    for text in [f'{city} погода на неделю', f'{city} купить квартиру']:
        """ Переходим в гугл """
        await page.goto('https://www.google.com/')
        await page.waitFor(random.randrange(3000, 5000))


        """ Забиваем поисковый запрос + гео """
        [[await page.type('input[class="gLFyf gsfi"]', i), await page.waitFor(random.randrange(100, 600))] for i in text]
        await page.keyboard.press('Enter')
        await page.waitFor(random.randrange(5000, 8000))

        """ Кликаем по выдаче """
        elemnt = await page.J('div.NJo7tc.Z26q7c.jGGQ5e > div > a > h3')
        await elemnt.click()
        await page.waitFor(random.randrange(3000, 6000))

        """ Имитируем действия на странице """
        for i in range(5):
            await page.keyboard.press(random.choice(['End', 'Home']))
            await page.waitFor(random.randrange(1000, 5000))

        await page.waitFor(random.randrange(3000, 6000))


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
async def registerMail(page):
    with open('FIO.txt', 'r', encoding = 'utf-8') as f:
        fio = f.read().split('\n')

    fio = random.choice(fio)
    _name = fio.split(' ')[0]
    _sname = fio.split(' ')[0]
    _mail = ''.join([dicKey[i] for i in fio if])
    _mail = _mail+str(random.randrange(1000, 10000))
    _password = 'Mad*s32Msasl'
    extra_mail = _mail+'@gmail.com'


    await page.goto('https://account.mail.ru/signup')
    await page.waitFor(random.randrange(3000, 6000))
    
    name = await page.waitForSelector('#fname')
    await name.type(_name)

    sname = await page.J('#lname')
    await sname.type(_sname)


    """ Выбрать день """
    elemnt = await page.J('div[data-test-id="birth-date__day"]')
    await elemnt.click()
    await page.waitFor(1500)
    
    selectElem = await page.J('div[data-test-id="select-menu-wrapper"]')
    selectElem = await selectElem.J('div')
    selectElem = await selectElem.JJ('div')
    await random.choice(selectElem).click()





    """ Выбрать месяц """
    elemnt = await page.J('div[data-test-id="birth-date__month"]')
    await elemnt.click()
    await page.waitFor(1500)
    selectElem = await page.J('div[data-test-id="select-menu-wrapper"]')
    selectElem = await selectElem.J('div')
    selectElem = await selectElem.JJ('div')
    await random.choice(selectElem).click()




    """ Выбрать год """
    elemnt = await page.J('div[data-test-id="birth-date__year"]')
    await elemnt.click()
    await page.waitFor(1500)

    selectElem = await page.J('div[data-test-id="select-menu-wrapper"]')
    selectElem = await selectElem.J('div')

    selectElem = await selectElem.JJ('span[class="base-0-2-61 control-0-2-69 auto-0-2-86"]')
    await random.choice(selectElem[20:40]).click()




    """ Мужской пол """
    await page.click('label[data-test-id="gender-male"]')

    """ Mail """
    [[await page.type('#aaa__input', i), await page.waitFor(random.randrange(100, 200))] for i in _mail]

    """ Password """
    [[await page.type('#password', i), await page.waitFor(random.randrange(100, 200))] for i in _password]
    [[await page.type('#repeatPassword', i), await page.waitFor(random.randrange(100, 200))] for i in _password]

    """ Переключить на резервнуб почту """ 
    # if await page.JJ('div[data-test-id="phone-number"]'):
    #     await page.click('a[data-test-id="phone-number-switch-link"]')
    # [[await page.type('#extra-email', i), await page.waitFor(random.randrange(100, 200))] for i in extra_mail]
    # await page.waitFor(random.randrange(1000, 3000))

    number_phone = smsAPI.getNumber(service='vk', country = 0)
    number_phone = number_phone['phone']

    """ Ввод номера телефона """
    [[await page.type('#phone-number__phone-input', i), await page.waitFor(100)] for i in number_phone[1:]]
    create = await page.JJ('button[data-test-id="first-step-submit"]')
    await create[-1].click()

    await page.waitFor(70*1000)
    if await page.JJ('a[data-test-id="resend-callui-link"]'):
        await page.click('a[data-test-id="resend-callui-link"]')

    

    """ Капча с картинкой """
    # elementIMG = await page.waitForSelector('img[data-test-id="captcha-image"]')
    # await elementIMG.screenshot({'path': 'capat.png'})
    # answerCapa = await ruCaptcha()
    # [[await page.type('input[placeholder="Код"]', i), await page.waitFor(300)] for i in answerCapa]
    # await page.click('button[data-test-id="verification-next-button"]')
    # await page.waitFor(100000)
    return

# a[data-test-id="resend-callui-timer"]
# a[data-test-id="resend-callui-link"]

async def ruCaptcha(img = 'capat.png'):
    connection = RuCaptchaConnection(token=RUCAPTCHA_KEY)          
    captcha_file = open(img, 'rb')
    captcha = connection.send(captcha_file)
    decision = captcha.wait_decision()

    return decision





async def main(key, url):
    page, browser = await open_browser(url)
    if not page: return 'Browser not found'
    # await warmingUpProfile(page)

    await registerMail(page)
    await closeAndDelete(key)
    return





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


