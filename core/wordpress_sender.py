import random
import sys

import mariadb
import requests

from core import tomtop_parser


class WordpressSender:
    _mariadb_sql_query = f"""INSERT INTO wp_posts (ID, post_author, post_date, 
                                    post_date_gmt, post_content, post_title, 
                                    post_excerpt, post_status, comment_status, 
                                    ping_status, post_password, post_name, 
                                    to_ping, pinged, post_modified, 
                                    post_modified_gmt, post_content_filtered, 
                                    post_parent, guid, menu_order, 
                                    post_type, post_mime_type, comment_count) 
                                VALUES (NULL, 0, CURRENT_DATE, CURRENT_DATE, 
                                    '%s', '%s', '', 'publish', 'open', 'open', '', '%s', '', '', 
                                    CURRENT_DATE, CURRENT_DATE, '', '0', '%s', '0', 'post', '', '0') """

    def __init__(self):
        self._init_mariadb_connection()

    def _init_mariadb_connection(self):
        """Init mariadb connection"""
        try:
            self._connection = mariadb.connect(
                user="some_user",
                password="some_password",
                host="ip-address",
                port=3306,
                database="wordpress"
            )

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def create_wordpress_posts(self, content):
        cursor = self._connection.cursor()

        post_url = "http://samsepi01.com/wordpress/?p=" + str(random.SystemRandom().randint(0, 1000000000))
        cursor.execute(
            self._mariadb_sql_query % (
                self._create_content(content),
                content[tomtop_parser.key_result_title].replace("'", "`"),
                content[tomtop_parser.key_result_title].replace(" ", "")[:10].lower().replace("'", "`") + "-post",
                post_url
            )
        )
        self._connection.commit()
        print("All operations has completed successfully!")

        cursor.close()

    def _create_content(self, content):
        return self.create_image(content[tomtop_parser.key_result_regular_image]) + \
               f"\n\n<!-- wp:paragraph --><p>{content[tomtop_parser.key_result_subtitle]}</p><!-- /wp:paragraph -->" \
               f"<!-- wp:heading --> <h2>Product Description:</h2><!-- /wp:heading -->" \
               f"<!-- wp:paragraph --><p>{content[tomtop_parser.key_result_description]}</p><!-- /wp:paragraph -->" \
               f"<!-- wp:heading --> <h2>Prices:</h2><!-- /wp:heading -->" \
               f"<!-- wp:paragraph --><p>{content[tomtop_parser.key_result_regular_price]}</p><!-- /wp:paragraph -->" \
               f"<!-- wp:paragraph --><p>{content[tomtop_parser.key_result_sale_price]}</p><!-- /wp:paragraph -->" \
               f"<!-- wp:heading --> <h2>Ratings:</h2><!-- /wp:heading -->" \
               f"<!-- wp:paragraph --><p>{content[tomtop_parser.key_result_product_rating]}</p><!-- /wp:paragraph -->" \
               f"<!-- wp:heading --> <h2>Options:</h2><!-- /wp:heading -->" \
               f"<!-- wp:paragraph --><p>{content[tomtop_parser.key_result_product_options]}</p><!-- /wp:paragraph -->" \
               f"<!-- wp:heading --> <h2>Shipping methods:</h2><!-- /wp:heading -->" \
               f"{content[tomtop_parser.key_result_product_shipping]}"

    def create_image(self, image_link):
        return '<!-- wp:image {"id":136,"sizeSlug":"large","linkDestination":"none"} -->' + \
               f'<figure class="wp-block-image size-large"><img src="{image_link}" alt="" ' \
               f'class="wp-image-136"/></figure><!-- /wp:image -->'

    def upload_media(self, media_url):
        filename = media_url.split('/')[-1]
        response = requests.get(media_url)
        if response.status_code == 200:
            upload_url = 'http://192.168.100.12/wordpress/wp-content/uploads'
            headers = {"Content-Disposition": f"attachment; filename={filename}", "Content-Type": "image/jpeg"}
            return requests.post(upload_url, auth=('user', 'pwd'), headers=headers,
                                 data=response.content)

    def __del__(self):
        self._connection.close()
