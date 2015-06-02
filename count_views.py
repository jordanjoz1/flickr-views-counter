import flickrapi
import csv
import sys
import datetime
import argparse
import os

# environment variable keys
ENV_KEY = 'FLICKR_API_KEY'
ENV_SECRET = 'FLICKR_API_SECRET'

MAX_PHOTOS_PER_PAGE = 500

# column headers for output file
columns = ['Title', 'Upload date', 'photo_id', 'url', 'Description',
           'View count', 'Favs count', 'Comments count']

# setup flickr api
flickr = None


def main():
    global flickr

    # parse arguments
    userId, fname, api_key, api_secret = parseArgs()

    # check if user provided api key/secret
    if not api_key or not api_secret:

        # try to get key/secret from environment variables
        api_key = os.getenv(ENV_KEY)
        api_secret = os.getenv(ENV_SECRET)

        # exit if we still dont' have key/secret
        if not api_key or not api_secret:
            sys.exit('No Flickr API key and secret. Either provide the key '
                     'and secret as options (--key and --secret) or set them '
                     'as environment variables.')

    # initialize flickr api
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    # get number of photos for the user
    userInfo = flickr.people.getInfo(user_id=userId)
    count = int(userInfo[0].find('photos').find('count').text)
    pages = count / MAX_PHOTOS_PER_PAGE + 1
    print('Counting views for %d photos...' % (count))

    # get list of photos
    photo_pages = []
    for page in range(1, pages + 1):
        photo_pages.append(
            flickr.photos.search(
                user_id=userId, per_page=str(MAX_PHOTOS_PER_PAGE), page=page))

    # get view count for each photo
    data = []
    for photo_page in photo_pages:
        for photo in photo_page[0]:
            data.append(get_photo_data(photo.get('id')))

    # write counts to output
    if (fname is not None):
        rows = create_rows_from_data(data)
        write_to_csv(fname, columns, rows)
        print('Photo data successfully written to %s (this could take hours '
              'if you have hundreds of photos)' % (fname))

    # display view count for photos
    print('Total photo views: %d' % (calc_total_views_from_data(data)))


def parseArgs():
    # parse arguments and do error checking
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id',
                        help='The id of the user whose total views will be '
                             'counted.',
                        default='.')
    parser.add_argument('--output',
                        help='Name of the output file',
                        default=None)
    parser.add_argument('--key',
                        help='Flickr API key (use once for setup)',
                        default=None)
    parser.add_argument('--secret',
                        help='Flickr API secret (use once for setup)',
                        default=None)
    args = parser.parse_args()
    return args.user_id, args.output, args.key, args.secret


def calc_total_views_from_data(data):
    total = 0
    for photo in data:
        total += int(photo['info'][0].attrib['views'])
    return total


def create_rows_from_data(data):
    rows = []
    for photo in data:
        title = photo['info'][0].find('title').text
        upload_date = photo['info'][0].get('dateuploaded')
        upload_date = datetime.datetime.fromtimestamp(
            int(upload_date)).strftime('%Y-%m-%d %H:%M:%S')
        photo_id = photo['info'][0].get('id')
        url = photo['info'][0].find('urls')[0].text
        description = photo['info'][0].find('description').text
        if description is None:
            description = ''
        views = photo['info'][0].get('views')
        favs = photo['favs'][0].get('total')
        comments = photo['info'][0].find('comments').text

        # output as delimited text
        row = [title, upload_date, str(photo_id), url, description,
               str(views), str(favs), str(comments)]
        rows.append(row)
    return rows


def get_photo_data(photo_id):
    info = flickr.photos.getinfo(photo_id=photo_id)
    favs = flickr.photos.getFavorites(photo_id=photo_id)
    return {'info': info, 'favs': favs}


def write_to_csv(fname, header, rows):
    with open(fname, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for row in rows:
            csvwriter.writerow(
                [s.encode("utf-8").replace(',', '').replace('\n', '')
                 for s in row])


if __name__ == "__main__":
    main()
