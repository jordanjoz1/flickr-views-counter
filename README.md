flickr-views-counter
====================

Python script to count the total number of views across all of a user's photos.  Flickr's API doesn't give a total photo count anymore, so this script makes use of [this very helpful library](http://stuvel.eu/flickrapi) to add up the counts for each photo and output the total number of views for a user.

##Steps to setup script
1. Make sure that your computer has [Python installed](https://www.python.org/downloads/)
2. Install the [Python Flickr API kit](http://stuvel.eu/flickrapi) using pip

  ```python
  pip install flickrapi
  ```
3. Get a [**Non-commercial** Flickr API key](https://www.flickr.com/services/apps/create/noncommercial/?).
  - Fill out the form
  - Keep the page with your new *key* and *secret* open, you'll need them in a moment
4. Download the [count-views.py](./count-views.py) script
  - Open your downloaded copy of `count-view.py` with a text editor
  - In your text editor, replace [`XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`](./count-views.py#L7) with your key (leave the quotation marks)
  - Similarly, replace [`YYYYYYYYYYYYYYYYYYYYYYY`](./count-views.py#L8) with your secret

##Running the script
Run the script with your **user id**.  For example, my user id is `26119226@N04`, which is the last part of the url for my photostream [https://www.flickr.com/photos/26119226@N04/](https://www.flickr.com/photos/26119226@N04/). 

So, I would run:
```python
./count-views.py 26119226@N04
```

If you want to save the data for your photos in csv format, then add an output file name. For example:
```python
./count-views.py 26119226@N04 --output photo-views.csv
```
###Get daily stats
If you're familiar with crontab, you can set the script up to save your daily photo statistics.  Here is an example that would run at noon every day, write the csv output to a folder with the date stamp, and log the total counts.  The actual implementation would vary slightly based on your paths, and, of course, your user id.

```bash
00 12 * * * python count-views.py 26119226@N04 --output ./flickr-counts/count-views-$(date +%F).csv >> flickr-counts-log.txt
```

### Options

#### -h, --help
Prints help message.

#### --output
Name of the output csv file to save photo data. Like, `photo-views.csv`

## FAQ
**Q:  why isn't there a website to do this for me?**
*A: The FlickrApi is [rate limited](https://developer.yahoo.com/forum/YQL/What-is-the-maximum-flickr-API/1361494903655-6a1e3a51-cd41-411e-86a9-dc2dee898ab5/) to 3600 queries per house, so a single API key wouldn't be able to handle requests for a large number of users*
