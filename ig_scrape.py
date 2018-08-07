import asyncio
from pyppeteer import launch
import time
import urllib
import os
import re

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

async def scrape_image(page, imageSelector):
    image = await page.evaluate("(element) => element.getAttribute('src')", imageSelector)
    return image

async def scrape_video(page, videoSelector):
    image = await page.evaluate("(element) => element.getAttribute('src')", videoSelector)
    return image

async def image_selector_function(page):
    modal = await page.querySelector('._97aPb ')
    imageSelector = await modal.querySelector('.FFVAD')
    return imageSelector

async def video_selector_function(page):
    modal = await page.querySelector('._97aPb ')
    videoSelector = await modal.querySelector('.tWeCl')
    return videoSelector

async def get_post_content(page, target):
    videoPlayButton = await video_button_function(page)
    print(videoPlayButton)
    if videoPlayButton:
        videoSelector = await video_selector_function(page)
        video = await scrape_video(page, videoSelector)
        print(video)
        urllib.request.urlretrieve(video, './' + target + '/' + video[video.rfind('/') + 1:])
    else:
        imageSelector = await image_selector_function(page)
        image = await scrape_image(page, imageSelector)
        print(image)
        urllib.request.urlretrieve(image, './' + target + '/' + image[image.rfind('/')+1: ])

async def video_button_function(page):
    modal = await page.querySelector('._97aPb ')
    videoPlayButton = await modal.querySelector('.videoSpritePlayButton')
    return videoPlayButton

async def scrap_story(page):
    await page.click("div[class='RR-M- h5uC0']")
    await page.waitForSelector(".yS4wN ")
    stories = await page.querySelectorAll('.-Nmqg')
    print(len(stories))
    for i in stories:
        modal = await page.querySelector('.GHEPc')
        imageSelector = await modal.querySelector('.i1HvM ')
        image = await page.evaluate("(element) => element.getAttribute('src')", imageSelector)
        print(image)
        await page.click("button[class='.ow3u_']")
        time.sleep(1)

async def page_one(browser, target):
    page = await browser.newPage()
    await page.setViewport({ 'width': 1280, 'height': 926 })
    await page.goto('https://www.instagram.com/' + target + '/?hl=en')

    # page_two = await browser.newPage()
    # await page_two.setViewport({ 'width': 1280, 'height': 926 })
    # await page_two.goto('https://www.instagram.com/' + target + '/?hl=en')
    # story = await page_two.querySelector('.h5uC0')
    # print(story)

    # if story:
    #     await scrap_story(page_two)

    createFolder('./' + target)

    totalPosts = int([await page.evaluate("(element) => element.textContent", i) for i in await page.querySelectorAll('.g47SY ')][0].replace(',', ''))

    await page.click("div[class='v1Nh3 kIKUG  _bz0w']")

    await page.waitForSelector(".D1AKJ")

    for i in range(totalPosts):
        rightButton = await page.querySelector('.coreSpriteRightChevron')

        if rightButton:
            photosCarousel = await page.querySelectorAll('.Yi5aA ')
            for i in range(len(photosCarousel)):
                await get_post_content(page, target)
                if i < len(photosCarousel) - 1:
                    await page.click("a[class='SWk3c  Zk-Zb coreSpriteRightChevron']")
                time.sleep(2)
        else:
            await get_post_content(page, target)
        
        await page.click("a[class='HBoOv coreSpriteRightPaginationArrow']")
        time.sleep(3)

    time.sleep(3)


async def page_two(browser, target):
    page = await browser.newPage()
    await page.setViewport({ 'width': 1280, 'height': 926 })
    await page.goto('https://www.instagram.com/' + target + '/?hl=en')
    story = await page.querySelector('.h5uC0')
    print(story)

    if story:
        await scrap_story(page)

async def browser_launch(target):
    browser = await launch({'headless': False, 'slowMo': 1})
    
    await page_one(browser, target)

    await browser.close()

asyncio.get_event_loop().run_until_complete(browser_launch('target'))