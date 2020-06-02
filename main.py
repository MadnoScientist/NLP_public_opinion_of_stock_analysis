from Spider import Spider
from post_create import post_create



def main():
    s = Spider()
    s.get_all_htmls()
    post_create()