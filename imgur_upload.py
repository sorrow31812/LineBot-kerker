from imgurpython import ImgurClient
from config import Client_ID, Client_Secret, Album_ID, Access_Token, Refresh_Token


def main(img_url):
    client = ImgurClient(Client_ID, Client_Secret, Access_Token, Refresh_Token)
    config = {
        'album': Album_ID
    }
    print("Uploading image... ")
    image = client.upload_from_url(img_url, config=config, anon=False)
    # print(image['link'])
    return image['link']


if __name__ == "__main__":
    main()
