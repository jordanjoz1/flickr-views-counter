import flickrapi
import csv
import sys
import datetime

# FILL THESE VALUES IN
api_key = u'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
api_secret = u'YYYYYYYYYYYYYYYYYYYYYYY'

# column headers for output file
columns = ['Title', 'Upload date', 'photo_id', 'url', 'Description', 'View count', 'Favs count', 'Comments count']

# setup flickr api
flickr = flickrapi.FlickrAPI(api_key, api_secret)

def main(userId, fname=None):
	
	# get list of photos
	photos = flickr.photos.search(user_id=userId, per_page='1000')
	
	# get view count for each photo
	data = []
	for photo in photos[0]:
		data.append(get_photo_data(photo.get('id')))
		
	# write counts to output
	if (fname is not None):
		rows = create_rows_from_data(data)
		write_to_csv(fname, columns, rows)
		print 'Photo data successfully written to %s' % (fname)
	
	# display view count for photos
	print 'Total photo views: %d' % (calc_total_views_from_data(data))

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
        upload_date = datetime.datetime.fromtimestamp(int(upload_date)).strftime('%Y-%m-%d %H:%M:%S')    
        photo_id = photo['info'][0].get('id')
        url = photo['info'][0].find('urls')[0].text
        description = photo['info'][0].find('description').text
        if description is None:
            description = ''
        views = photo['info'][0].get('views')
        favs = photo['favs'][0].get('total')
        comments = photo['info'][0].find('comments').text

        # output as delimited text
        row=[title,upload_date,str(photo_id),url,description,str(views),str(favs),str(comments)]
        rows.append(row)
    return rows
	
def get_photo_data(photo_id):
    info = flickr.photos.getinfo(photo_id=photo_id)
    favs = flickr.photos.getFavorites(photo_id=photo_id)
    return {'info': info, 'favs': favs}
	
def write_to_csv(fname, header, rows):
    with open(fname, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for row in rows:
            csvwriter.writerow([s.encode("utf-8").replace(',', '').replace('\n','') for s in row])
			
if __name__ == "__main__":
	argc = len(sys.argv)
	if argc == 2:
		main(sys.argv[1])
	elif argc == 3:
		main(sys.argv[1], sys.argv[2])
	else:
		sys.exit('Usage: %s <user-id> [output-file-name]' % (sys.argv[0]))