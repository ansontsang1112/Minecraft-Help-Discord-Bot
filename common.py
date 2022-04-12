import string

from bs4 import BeautifulSoup


def getIDInfo(className: string, html: string):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        related = soup.find_all(id=className)
        for r in related:
            return r.text
    except Exception as e:
        return e


def getClassInfo(tag: string, className: string, html: string):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return soup.find(tag, class_=className).text.split("\n")[1]
    except Exception as e:
        return e


def getAllClassInfo(tag: string, className: string, html: string):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return soup.find_all(tag, class_=className)
    except Exception as e:
        return e
