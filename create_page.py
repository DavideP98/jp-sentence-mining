import sys
import re
import pysubs2
from furigana import to_html
from jinja2 import Environment, FileSystemLoader, select_autoescape

# TODO 
# - add support for files that don't have an episode number
# - find a way to make language handling modular
# - use generator functions if possible 
def make_title(filepath):
    pattern = r'(.*/)?([0-9]+)?_([^/]+)\.ass$'
    match = re.search(pattern, filepath)
    if match:
        ep_number = match.group(2)
        ep_title = match.group(3)
        return f"Episode {ep_number}: {ep_title}"
    return None

def create_page(movie_data):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("movie_page.html")
    print(template.render(movie_data=movie_data))

def sub_extract(filepath, audio_path):
    subs = pysubs2.load(filepath, encoding="utf-8")
    movie_data = {
        "title": "",
        "audio": "",
        "dialogues": []
    }
    for line in subs:
        if "♪" not in line.text and not re.match("（.*[音,声].*）", line.text):
            text = line.text.replace("\\N", " ")
            html = to_html(text)
            result = re.match(r'^（[^（）]+）', html) 
            meta = ""
            html_text = html
            if result:
                html_text = html[result.span()[1]:]
                meta = result.group()
            movie_data['dialogues'].append(dict(meta=meta,
                start=line.start, end=line.end, text=html_text))
    movie_data['title'] = make_title(filepath)
    movie_data['audio'] = audio_path
    
    return movie_data

def main():
    argn = len(sys.argv)
    if argn < 2:
        print("Usage: python extract_script.py <path-to-subtitle-file>")
        sys.exit(1)
    path_to_sub = sys.argv[1]
    path_to_audio = None
    if argn == 3:
        path_to_audio = sys.argv[2]
    create_page(sub_extract(path_to_sub, path_to_audio))


if __name__ == "__main__":
    main()
