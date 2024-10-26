import time, requests, sys, time, os, argparse

# List of features for video snippet
snippet_features = ["title", "publishedAt", "channelId", "channelTitle", "categoryId"]

# List of features for channel information
channel_features = ["channel_creation_date", 
                    "channel_subscriber_count", "channel_video_count", 
                    "channel_description", "channel_image", "channel_country", 
                    "channel_total_views", "channel_keywords", 
                    "channel_url"]

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

# Headers for the CSV
header = ["video_id"] + snippet_features + ["video_url", "trending_date", "tags", "view_count", "likes",
                                            "comment_count", "thumbnail_link", "comments_disabled", 
                                            "ratings_disabled", "description"] + channel_features

'''
# Gerar colunas dos comentários na sequência correta
for i in range(0):
    header += [f"comment_{i+1}_author", f"comment_{i+1}_content", f"comment_{i+1}_likes"]
'''
    
def setup(api_path, code_path):
    with open(api_path, 'r') as file:
        api_key = file.readline().strip()

    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return api_key, country_codes

def prepare_feature(feature):
    # Removes any unsafe characters and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'

def api_request(page_token, country_code):
    # Builds the URL and requests the JSON from the API
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    try:
        request = requests.get(request_url, timeout=10)
        request.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\033[0;31mFailed to fetch data for {country_code}: {e}")
        return None
    return request.json()

def get_channel_data(channel_id):
    # Fetch channel data such as creation date, subscriber count, and total video count
    request_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,brandingSettings&id={channel_id}&key={api_key}"
    try:
        request = requests.get(request_url, timeout=10)
        request.raise_for_status()
        channel_data = request.json().get("items", [{}])[0]
    except requests.exceptions.RequestException as e:
        print(f"\033[0;31mFailed to fetch channel data for {channel_id}: {e}")
        return ["N/A"] * 10
    
    snippet = channel_data.get("snippet", {})
    statistics = channel_data.get("statistics", {})
    branding = channel_data.get("brandingSettings", {})
    
    # Data points from the API response
    channel_creation_date = snippet.get("publishedAt", "")
    subscriber_count = statistics.get("subscriberCount", "N/A")
    video_count = statistics.get("videoCount", "N/A")
    channel_description = snippet.get("description", "N/A")
    channel_image = snippet.get("thumbnails", {}).get("default", {}).get("url", "N/A")
    country = snippet.get("country", "N/A")
    total_views = statistics.get("viewCount", "N/A")
    keywords = branding.get("channel", {}).get("keywords", "N/A")
    
    # Default URL: Manually create the standard YouTube channel URL using the channel ID
    channel_url = f"https://www.youtube.com/channel/{channel_id}"

    return [channel_creation_date, subscriber_count, video_count, channel_description, 
            channel_image, country, total_views, keywords, channel_url]

'''
def get_comments(video_id):
    number_of_comments = 1

    # Fetch up to 5 top comments for a given video
    request_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResults={number_of_comments}&order=relevance&key={api_key}"
    try:
        request = requests.get(request_url, timeout=10)
        request.raise_for_status()
        comments = request.json().get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"\033[0;31mFailed to fetch comments for {video_id}: {e}")
        comments = []
    
    comment_data = []
    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        author = snippet.get('authorDisplayName', '[unknown]')
        text = snippet.get('textDisplay', '[no comment]')
        like_count = snippet.get('likeCount', 0)
        comment_data.append((author, text, like_count))
    
    # Ensure we always have exactly 5 comments (fill missing ones with default values)
    while len(comment_data) < number_of_comments:
        comment_data.append(("[none]", "[no comment]", 0))
    
    return comment_data
'''

def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string separated by pipe character
    return prepare_feature(",".join(tags_list))

def get_videos(items):
    lines = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False

        # Skip videos without statistics (often deleted)
        if "statistics" not in video:
            continue

        video_id = prepare_feature(video['id'])
        snippet = video['snippet']
        statistics = video['statistics']

        # Video snippet features
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]

        # Special case features
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)

        # Handle likes/dislikes and comments
        likes = statistics.get('likeCount', 0)
        if likes == 0:
            ratings_disabled = True

        comment_count = statistics.get('commentCount', 0)
        if comment_count == 0:
            comments_disabled = True

        # Get channel data (pass the channelTitle as well)
        channel_data = get_channel_data(snippet['channelId'])

        # Get comments data
        #comments_data = get_comments(video['id'])
        #comments_flat = [prepare_feature(comment) for comment_tuple in comments_data for comment in comment_tuple]

        # Compile all the data into a CSV line
        line = [video_id] + features + [prepare_feature(x) for x in [video_url, trending_date, tags, view_count, likes,
                                                                       comment_count, thumbnail_link, comments_disabled,
                                                                       ratings_disabled, description]] + \
               [prepare_feature(x) for x in channel_data] #+ comments_flat

        lines.append(",".join(line))
    return lines

def get_pages(country_code, next_page_token="&"):
    country_data = []
    while next_page_token is not None:
        video_data_page = api_request(next_page_token, country_code)
        if video_data_page is None:
            break
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token else None
        items = video_data_page.get('items', [])
        country_data += get_videos(items)
    return country_data

def write_to_file(country_code, country_data):
    print(f"\033[0;32mWriting {country_code} data to file...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(f"{output_dir}/{time.strftime('%y.%d.%m')}_{country_code}_videos.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")

def get_data():
    for country_code in country_codes:
        country_data = [",".join(header)] + get_pages(country_code)
        write_to_file(country_code, country_data)

if __name__ == "__main__":
    # Marcar o tempo de início
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', help='Path to the file containing the api key', default='api_key.txt')
    parser.add_argument('--country_code_path', help='Path to the file containing the list of country codes', default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the output files', default='output/')
    args = parser.parse_args()

    output_dir = args.output_dir
    api_key, country_codes = setup(args.key_path, args.country_code_path)
    get_data()

    # Marcar o tempo de término
    end_time = time.time()

    # Calcular o tempo total
    total_time = end_time - start_time

    # Exibir o tempo total formatado em horas, minutos e segundos
    print(f"\033[0;36mRuntime: {(total_time % 3600) // 60} minutes and {total_time % 60:.2f} seconds\033[m")
