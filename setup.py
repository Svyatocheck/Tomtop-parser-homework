from core.tomtop_parser import TomtopShopParser
from core.wordpress_sender import WordpressSender


def main():
    input_url = input("Product link from Tomtop's website: ")
    print("Parse product site ...")
    content_dictionary = TomtopShopParser(input_url).get_content()
    print("Send results to Wordpress...")
    sender = WordpressSender().create_wordpress_posts(content_dictionary)
    print("Done.")


if __name__ == '__main__':
    main()
