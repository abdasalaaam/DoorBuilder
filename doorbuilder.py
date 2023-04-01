from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import time
import pickle
import atexit

options = Options()
options.add_argument("--headless")
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['acceptInsecureCerts'] = True 
driver = ''

types = ['raised', 'stamped carriage', 'shaker', 'sterling', 'planks', 'skyline', 'shoreline', 'overlay', 'full', 'recessed']

colors = ['almond with', 'sandstone with','bronze with', 'white', 'almond', 'sandstone', 'brown', 'bronze', 'gray', 'desert', 'black', 'classic woodgrain', 'modern woodgrain',
'evergreen', 'dark bronze','charcoal', 'ivory', 'mocha', 'solar', 'anodized', 'graphite', 'cedar', 'mahogany', 'dark oak', 'natural oak', 'driftwood'
, 'walnut', 'carbon oak']

inserts = ['no inserts', 'cascade', 'prairie', 'sherwood', 'waterton', 'stockton', '3 piece sunburst','2 piece sunburst','4 piece sunburst', '2 piece arched stockton', '4 piece arched madison', '4 piece arched stockton', 'arched stockton',
 'sunburst', 'cathedral', '2 piece arched madison', 'arched madison', 'madison']

glasses = ['clear','aluminum','plain stockton', 'plain madison', 'plain','tinted stockton','tinted madison',
'tinted','glue chip madison', 'glue chip stockton','seeded madison', 'seeded stockton', 'glue chip', 'frosted', 'polycarbonate', 'obscure', 'seeded', 'faux stockton' , 'faux madison', 'faux', 'double pane']

windowRows = ['no windows', 'first', 'second','top 2', 'top','all', 'left', 'right', 'double', 'bottom 2', 'bottom']

designs = ['short', 'long', 'oversized', 'shaker', 'flush', 'accents', 'full', '10a', '10', '11a', '11', '12a', '12', '33a', 
'33', '34a', '34', '35a', '35', '30a', '30', '31a', '31', '32a', '32', '13a', '13', '14a', '14','15a','15']

thermals = ['17.54','R17', '12.35','r12', 'noninsulated', 'non-insulated', 'steelback insulated', 'steelback','non', 'vinyl']

models = [2518, 2583,2551,2550,'2540D',2128,2127,2141,2151,2140,2150,'2140D',2328,2327,2717, 5216,
5283,5251,5250,'5240D',2216,2206,2283,2241,2251,2240,2250,'2240D',5602,5600,5300,2298,5800,5500,'3297R', '3295R']

hardware = ['handles','decorative','hardware','exterior', 'magnetic', 'spade','BARCELONA PULL RINGS AND CORNER BRACKETS','WROUGHT IRON HANDLES AND HINGES','STANDARD BARCELONA HANDLES AND HINGES','STANDARD DECORATIVE SPADE HANDLES AND HINGES',
'STANDARD BARCELONA HANDLES','STANDARD BARCELONA HINGES','BARCELONA PULL RINGS','BARCELONA CORNER BRACKETS','WROUGHT IRON HANDLES','WROUGHT IRON HINGES','STANDARD DECORATIVE SPADE HANDLES','STANDARD DECORATIVE SPADE HINGES','MAGNETIC SPADE HANDLES','MAGNETIC SPADE HINGES','MAGNETIC SPADE HANDLES AND HINGES']

styles = ['steel', 'wood', 'fiberglass', 'overlay']


help = "Welcome to the Ace's Garage Door automated door builder. To build the design for the door you want, all you have to do is send the specifications (size, color, insulation, design, windows etc.) in one message, in any order. For example: \n 16x7 white steelback insulated raised short panel cathedral windows plain glass first row\n This will send you a link back to the door designed with those specs. For more help with specific doors/specifications, please send the word 'more'."
more = "For overlay doors, you must put the specific design number, for example 12a. For insulation, you can either put the model number (eg. 2216), the type of insulation (eg. vinyl), or the R-value (eg. R-9.65). For windows, you can say where the windows are located (eg. the first row), the type of glass (eg. obscure), and insert design (eg. stockton). If you do not want windows, you can simply omit mentioning windows. For doors that can have hardware, you can add it with either the hardware you want or just the word 'decorative'. For specific sizes, you can put either symbols for units or the words (ie. 15'10\"x6'9\" or 15 feet 10 inches by 6 feet 9 inches)."

cardlink = ''

class DoorBuilder:
    cardlink = ''
    def __init__(self, driver):
        self.driver = driver

    def build(self, specifications):
        door = getDoorFromText(specifications)
            #sends an error message if size is wrong
        if isinstance(door, str):
            return door
        cached = isDoorCached(door)
        if cached:
            time.sleep(1)
            return cached
        print('started')

        print('page loaded')
        if self.driver.page_source.__contains__('BVID__59'):
            tags = {
                'dims': ['__BVID__59','__BVID__60','__BVID__61','__BVID__62'],
                'dimWait' : '__BVID__59',
                'prodWait' : 'section-timeless__BV_tab_controls_',
                'desWait' : '__BVID__255___BV_tab_button__',
                'styleWait' : '__BVID__382___BV_tab_button__',
                'insWait' : '__BVID__265___BV_tab_button__',
                'colWait' : '__BVID__304___BV_tab_button__',
                'col2Wait' : '__BVID__308___BV_tab_button__',
                'winWait' : '__BVID__340___BV_tab_button__',
                'decWait' : '__BVID__223___BV_tab_button__'
            }
        else:
            tags = {
                'dims': ['__BVID__51','__BVID__52','__BVID__53','__BVID__54'],
                'dimWait' : '__BVID__51',
                'prodWait' : '__BVID__60___BV_tab_button__',
                'desWait' : '__BVID__133___BV_tab_button__',
                'styleWait' : '__BVID__261___BV_tab_button__',
                'insWait' : '__BVID__143___BV_tab_button__',
                'colWait' : '__BVID__169___BV_tab_button__',
                'col2Wait' : '__BVID__173___BV_tab_button__',
                'winWait' : '__BVID__205___BV_tab_button__',
                'decWait' : '__BVID__301___BV_tab_button__'
            }
        url = fullBuild(self, door, tags, self.driver)
        return url

    def waitForCardLinkToChange(self,driver, time = 10):
        try:       
            wait = WebDriverWait(driver,time)
            img = wait.until(lambda a: self.setCurrentCardLink())
            return 0
        except:
            try:
                #wait = WebDriverWait(driver,8)
                #img = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'modal-body')))
                for i in driver.find_elements(By.CLASS_NAME, 'modal-body'):
                    if i.is_displayed():
                        return i.text
                return 1
            except:
                return 1

    def setCurrentCardLink(self):
        navs = self.driver.find_elements(By.CLASS_NAME, 'card-link')
        displayedCards = []
        for n in navs:
            if n.is_displayed() and n.get_attribute('title'):
                if n.get_attribute('title') == self.cardlink:
                    return False
                self.cardlink = n.get_attribute('title')
                return True
                #displayedCards.append(n)
        '''if len(displayedCards) > 0:
            dtitle = displayedCards[0].get_attribute('title')
            if not dtitle == cardlink:
                cardlink = dtitle
                return True'''
        return False

    def resetDriver(self):
        keep_open = self.driver.window_handles[0]
        for handle in self.driver.window_handles:
            if handle != keep_open:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(keep_open)
        self.driver.get('https://doorvisions.chiohd.com/')

def waitForElement(element, by, driver,time = 22):
    try:
        wait = WebDriverWait(driver,time)
        img = wait.until(ec.visibility_of_element_located((by,element)))
        return 0
    except:
        try:
            #wait = WebDriverWait(driver,8)
            #img = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'modal-body')))
            for i in driver.find_elements(By.CLASS_NAME, 'modal-body'):
                if i.is_displayed():
                    return i.text
            return 1
        except:
            return 1



def getElement(by, element, driver):
    return driver.find_element(by, element)

def findElementLookingFor(clas, content, driver):
    eles = driver.find_elements(By.CLASS_NAME, clas)
    for element in eles:
        if content.lower() in element.text.lower():
            return element
    if len(eles) > 0:
        return eles[0]
    else:
        return 'Element not found'

def findButtonForSpec(spec, clas, driver, k = 0):
    eles = driver.find_elements(By.CLASS_NAME, clas)
    possEles = []
    for ele in eles:
        if ele.get_attribute('title'):
            if ele.is_displayed():
                possEles.append(ele)
    for p in possEles:
        title = p.get_attribute('title')
        for s in spec:
            if str(s).lower() in title.lower():
                return p
    if k < 5:
        time.sleep(.1)
        return findButtonForSpec(spec, clas, driver, k=k + 1)
    if len(possEles) > 0:
        return possEles[0]
    if k < 10:
        time.sleep(.1)
        return findButtonForSpec(spec, clas, driver, k=k + 1)
    return ''

def startDriver():
    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
    driver.get('https://doorvisions.chiohd.com/')
    return driver
    #partyid = driver.execute_script('return accountdata.$partyId.val();')

def clearAndSend(element, word):
    element.clear()
    element.send_keys(word)

def fillDimensions(tags, door, driver):
    clearAndSend(getElement(By.ID, tags[0], driver),door['width'])
    clearAndSend(getElement(By.ID, tags[1], driver),door['winches'])
    clearAndSend(getElement(By.ID, tags[2], driver),door['height'])
    clearAndSend(getElement(By.ID, tags[3], driver),door['hinches'])
    findElementLookingFor('btn-primary','confirm size', driver).click()

def completeAndReturnPDF(driver, door):
    findElementLookingFor('overflow-ellipsis', 'summary', driver).click()
    time.sleep(.3)
    findElementLookingFor('btn-primary', 'download', driver).click()
    switchToNewTab(driver)
    print('switched to new tab')
    if not waitForElement('pageContent', By.CLASS_NAME, driver):
        print(driver.current_url)
        cached_urls.update({convertDoorToString(door):driver.current_url})
        return driver.current_url
    else:
        return 'PDF did not load'
        
def isDoorCached(door):
    c = convertDoorToString(door)
    if c in cached_urls:
        return cached_urls[c]
    else: return 0

def convertDoorToString(door):
    s = ''
    for i in door:
        s += str(door[i])
    return s

def fullBuild(builder, door, tags, driver):
    w = waitForElement(tags['dimWait'], By.ID,driver)
    if not w:
        fillDimensions(tags['dims'], door, driver)
    else:
        return 'Failure in measurements selection' if w == 1 else w
    print('measurements filled')
        #products section
    w = builder.waitForCardLinkToChange(driver)
    if not w:
        try:
            findButtonForSpec(door['type'], 'card-link',driver).click()
        except:
            return 'Failure in door product selection'
    else:
        return 'Failure in door product selection' if w == 1 else w

    if door['style'][0] and (door['type'][0] == 'shoreline' or door['type'][0] == 'overlay'):
        builder.waitForCardLinkToChange(driver)
        if not w:
            try:
                findButtonForSpec(door['style'], 'card-link', driver).click()
            except:
                return 'Failure in door style selection (wood, steel, or fiberglass)'
    
        #design section
    w = builder.waitForCardLinkToChange(driver)
    if not w:
        try:
            findButtonForSpec(door['design'], 'card-link', driver).click()
        except:
            return 'Failure in door design selection'
    else:
        return 'Failure in door design selection' if w == 1 else w

        #insulation
    w = chooseInsulation(builder, door, driver)
    if w:
        return 'Failure in insulation selection' if w == 1 else w

        #color
    print('waiting for color cards')
    w = builder.waitForCardLinkToChange(driver)
    print('color cards appeared')
    if not w:
        print('finding button to click')
        col = findButtonForSpec(door['color'], 'card-link', getElement(By.ID,'items-collapser-Solid Colors', driver))
        if col:
            print('found button')
            col.click()
            print('button clicked')
        else:
            print('wrong button')
            try:
                getElement(By.ID,tags['col2Wait'], driver).click()
                col = findButtonForSpec(door['color'], 'card-link', driver)
                if not col:
                    return 'Failure in door color selection'
                col.click() 
            except:
                return 'Failure in door color selection'
    else:
        return 'Failure in door color selection' if w == 1 else w
    print('color filled')
        #windows, inserts, glass
    print('waiting for window')
    w = builder.waitForCardLinkToChange(driver)
    print('windows appeared')
    if not w:
        try:
            findButtonForSpec(door['windows'], 'card-link', getElement(By.ID, 'items-collapser-Position', driver)).click()
            print('selected window')
            if not door['windows'][0].__contains__('no'):
                findButtonForSpec(door['glass'], 'card-link', getElement(By.ID, 'items-collapser-Glass', driver)).click()
                print('selected glass')
                if not (door['type'][0] == 'sterling' or door['type'][0] == 'full'):
                    findButtonForSpec(door['inserts'], 'card-link', getElement(By.ID, 'items-collapser-Window Inserts', driver)).click()
                    print('selected inserts')
        except:
            return 'Failure in window selection'
    else:
        return 'Failure in window selection' if w == 1 else w

    if not door['decor'][0] == 'omit':
        w = builder.waitForCardLinkToChange(driver,5)
        if not w:
            try:
                findButtonForSpec(door['decor'], 'card-link', driver).click()
            except:
                print('Hardware attempted, but failed')
    
    print('completed')
    return completeAndReturnPDF(driver, door)

def chooseInsulation(builder,door, driver):
    w = builder.waitForCardLinkToChange(driver)
    breakloop = False
    if not w:
        if not door['thermal'][0][0] == 'r':
            try:
                findButtonForSpec(door['thermal'], 'card-link', getElement(By.ID, 'items-collapser-Thermal Requirements / Construction', driver)).click()
            except:
                return 1
        else:
            eles = driver.find_elements(By.CLASS_NAME,'card-body')
            model = '10000'
            for t in door['thermal']:
                for e in eles:
                    try:
                        op = e.find_element(By.CSS_SELECTOR, 'output')
                    except:
                        continue
                    if t.lower() in op.text.lower():
                        print(op.text.lower())
                        h7 = e.find_element(By.CSS_SELECTOR, 'h7')
                        model = getNumFromString(h7.text)
                        print(model)
                        breakloop = True
                        break
                if breakloop == True:
                        break
            try:
                findButtonForSpec([model], 'card-link', getElement(By.ID, 'items-collapser-Thermal Requirements / Construction', driver)).click()
            except:
                return 1
        return 0
    else:
        return w

def clickAndCheckForError(element, driver):
    element.click()
    closes = driver.find_elements(By.CLASS_NAME, 'close')
    wait = WebDriverWait(driver,8)
    for c in closes:
        try:
            img = wait.until(ec.visibility_of_element_located(c))
        except:
            continue
        return getElement(By.ID,'__BVID__153___BV_modal_body_', driver).text
    return 0

def getNumFromString(s):
    word = ''
    for i in s:
        if i.isdigit():
            word += i
    return word

def switchToNewTab(driver):
    window_handles = driver.window_handles
    current_handle = driver.current_window_handle

    for handle in window_handles:
        if handle != current_handle:
            driver.switch_to.window(handle)
            break

def getDoorFromText(response):
    try:
        size = getSize(response)
    except:
        return 'Please check the size'
    response = size[1]
    size = size[0]
    glass = findSpecFromCategory(glasses, response.lower())
    insert = findSpecFromCategory(inserts, response.lower())
    if glass == 'double pane':
        glass = 'insulated'
    type = findSpecFromCategory(types, response.lower())
    return {
        'width' : size['width'],
        'height' : size['height'],
        'winches' : size['winches'],
        'hinches' : size['hinches'],
        'type' : type or ['raised'],
        'design' : findSpecFromCategory(designs, response.lower()) or ['short'],
        'style' : findSpecFromCategory(styles, response.lower()) or [''],
        'thermal' : findSpecFromCategory(models,response.lower()) or determineInsulation(response.lower()) or ['r-n'],
        'color' : findSpecFromCategory(colors, response.lower()) or ['white'],
        'windows' : findSpecFromCategory(windowRows, response.lower()) or (['no windows'] if glass == '' and insert == '' else ['first', 'single', 'top', 'full']),
        'glass' : glass or (['tinted'] if type == 'sterling' else ['plain','clear']),
        'inserts' : insert or ['no inserts'],
        'decor' : findSpecFromCategory(hardware, response.lower()) or ['omit']
    }

def determineInsulation(res):
    possibilities = {
        'best insulation' : ['r-16', 'r-17', 'r-18', 'r-19', 'r-v'],
        'heavy duty insulation' : ['r-16', 'r-17', 'r-18', 'r-19', 'r-v'],
        'flush' : ['r-10', 'r-1', 'r-9'],
        'skyline' : ['r-10', 'r-1', 'r-9'],
        'vinyl' : ['r-7', 'r-6'],
        '7.' : ['r-7'],
        '9.' : ['r-9'],
        'noninsulated' : ['r-n'],
        'non' : ['r-n'],
        '16.' : ['r-16'],
        '17.' : ['r-17'],
        '15.' : ['r-15'],
        '12.' : ['r-12'],
        '13.' : ['r-13'],
        '14.' : ['r-14'],
        'r-1' : ['r-1'],
        '18.' : ['r-18'],
        'steelback' : ['r-9', 'r-10', 'r-11', 'r-12', 'r-1', 'r-v'],
        'steel back' : ['r-9', 'r-10', 'r-11', 'r-12', 'r-1', 'r-v'],
        'double' : ['r-9', 'r-10', 'r-11', 'r-12', 'r-1', 'r-v'],
        'two sided' : ['r-9', 'r-10', 'r-11', 'r-12', 'r-1', 'r-v'],
        'insulated' : ['r-9', 'r-7', 'r-6', 'r-1', 'r-v']
    }
    for p in possibilities:
        if p in res:
            return possibilities[p]
    return ''

def findSpecFromCategory(cat, response):
    for word in cat:
        if str(word) in response:
            return [word]
    return ''

def getSize(dim_str):
    pattern = r"(\d+)(?:'|\s*feet\s*)?(\d*)?(?:\"|\s*inches\s*)?(?:x|\s*by\s*)(\d+)(?:'|\s*feet\s*)?(\d*)?(?:\"|\s*inches\s*)?"
    match = re.match(pattern, dim_str, re.IGNORECASE)
    if match:
        width_feet = int(match.group(1))
        width_inches = int(match.group(2) or '0')
        height_feet = int(match.group(3))
        height_inches = int(match.group(4) or '0')
        if width_feet < 3 or width_inches > 12 or height_feet < 3 or height_inches > 12:
            raise ValueError("Invalid dimension string format")
        dimensions = {
            'width': width_feet,
            'winches': width_inches,
            'height': height_feet,
            'hinches': height_inches
        }
        modified_str = re.sub(pattern, '', dim_str, re.IGNORECASE).strip()
        return dimensions, modified_str
    else:
        raise ValueError("Invalid dimension string format")

def saveURLs():
    with open('data.pkl', 'wb') as f:
        pickle.dump(cached_urls, f)

def loadURLs():
    try:
        with open('data.pkl', 'rb') as f:
            loaded_data = pickle.load(f)
            return loaded_data
    except FileNotFoundError:
        print("pickle file does not exist")
        return {}

cached_urls = loadURLs()
atexit.register(saveURLs)

#startDriver()
#print(build('16x7 noninsulated white raised long panel sunburst tinted windows'))


#potential use:

def waitForClassElement(clas, text, driver, time = 10):
    try:       
        findAndWaitElementWithText(clas,text,driver,time)
        return 0
    except:
        try:
            #wait = WebDriverWait(driver,8)
            #img = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'modal-body')))
            for i in driver.find_elements(By.CLASS_NAME, 'modal-body'):
                if i.is_displayed():
                    return i.text
            return 1
        except:
            return 1

def findAndWaitElementWithText(clas, texts, driver, t = 10, k = 0):
    wait = WebDriverWait(driver,t)
    eles = driver.find_elements(By.CLASS_NAME, clas)
    for i in eles:
        for text in texts:
            if text.lower() in i.text.lower():
                wait.until(ec.visibility_of(i))
                time.sleep(.5)
                return True
    if k < 100:
        time.sleep(0.1)
        return findAndWaitElementWithText(clas,text,driver,k= k + 1)
    raise Exception('Could not find element')