import re

input_text = """
- Users/N6506/Home/health/entertainment/news_underground/games/created/game/**
- Users/N6506/Home/health/entertainment/news_underground/games/downloaded/tools/Translator++/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/programs/mediaSorter_Python/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/programs/mediaSorter_Python-1/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/programs/my_flutter_app/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/programs/PWA_app/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/programs/video_player/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/programs/vs_media-player/**
- Users/N6506/Home/health/vue/clock/**
- Users/N6506/Home/travail/Polytech Paris Saclay/stage et5/activities/**
- Users/N6506/Home/travail/Polytech Paris Saclay/stage et5/codes/france.tv-tanuki-free/**
- Users/N6506/Home/travail/Polytech Paris Saclay/stage et5/reporting/**

- Users/N6506/Home/health/entertainment/videos/**/*.*
- Users/N6506/Home/health/entertainment/news_underground/games/downloaded/to_scan/*/**
- Users/N6506/Home/health/entertainment/news_underground/mediaSorter/media/**/*.*
- Users/N6506/Home/travail/Polytech Paris Saclay/stage et5/records/**

+ Users/N6506/Home/**
- **
"""

def convert_to_windows_paths(text):
    paths = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('+'):
            continue  # ignore empty lines and + lines

        if line.startswith('- '):
            path = line[2:]  # remove "- "
        elif line.startswith('-'):
            path = line[1:]  # remove "-" without space
        else:
            continue

        # Remove trailing /**, /*/**, /**/.*, etc.
        path = re.sub(r'/(\*\*|\*)/.*$', '', path)
        path = re.sub(r'/\*\*$', '', path)
        path = re.sub(r'/\*\.\*$', '', path)

        # Convert / to \ (Windows style)
        path = path.replace('/', '\\')

        # Quote if contains spaces
        if " " in path:
            path = f'"{path}"'

        paths.append(path)

    return "|".join(paths)

result = convert_to_windows_paths(input_text)
print(result)
