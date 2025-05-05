from typing import TextIO, Iterator
import re
from collections import defaultdict, Counter


"""1. python.magic_post_count"""
def count_magic_posts(stream: TextIO, min_owner_id: int, max_post_id: int) -> int:
    magic_post_count = 0
    pattern1 = r'(?<=OwnerUserId=)"[0-9]+"'
    pattern2 = r'(?<=Id=)"[0-9]+"'
    for line in stream:
        line = line.strip()
        if re.search(pattern1, line) and re.search(pattern2, line):
            if int(re.search(pattern1, line).group().strip('"')) > min_owner_id and int(re.search(pattern2, line).group().strip('"')) < max_post_id:
                magic_post_count += 1
    return magic_post_count

"""2. python.magic_users"""
def find_magic_users(stream:TextIO, max_post_id: int) -> set[int]: 
    pattern1 = r'(?<=OwnerUserId=)"[0-9]+"'
    pattern2 = r'(?<=Id=)"[0-9]+"'
    magic_users = {
        int(re.search(pattern1, line).group().strip('"'))
        for line in stream
        if re.search(pattern1, line) and re.search(pattern2, line)
        if int(re.search(pattern2, line).group().strip('"')) < max_post_id
    }
    return magic_users
"""3. python.view_count"""
def count_views(stream:TextIO) -> int:
    pattern_view = r'(?<=ViewCount=)"[0-9]+"'
    view_lst = [
        int(re.search(pattern_view, line).group().strip('"'))
        for line in stream
        if re.search(pattern_view, line)
    ]
    view_count = sum(view_lst)
    return view_count

"""4. python.magic_map"""
def build_magic_map(stream: TextIO) -> dict[int: set[str]]:
    pattern_tags = r'(?<=Tags=")[^"]+'
    pattern_id = r'(?<=Id=)"[0-9]+"'
    magic_map = {
        int(re.search(pattern_id, line).group().strip('"')): set(re.search(pattern_tags, line).group().replace('&lt;', ' ').replace('&gt;', ' ').split())
        for line in stream
        if re.search(pattern_tags, line) and re.search(pattern_id, line)
    }    
    return magic_map

"""5. python.tag_map"""
def build_tag_map(stream: TextIO) -> dict[str: set[int]]: 
    tag_map = defaultdict(set)
    pattern_tags = r'(?<=Tags=")[^"]+'
    pattern_id = r'(?<=Id=)"[0-9]+"'
    for line in stream: 
        line = line.strip()
        if re.search(pattern_tags, line) and re.search(pattern_id, line):
            id_tag = int(re.search(pattern_id, line).group().strip('"'))
            clear_tags = set(re.search(pattern_tags, line).group().replace('&lt;', ' ').replace('&gt;', ' ').split())
            for tag in clear_tags:
                tag_map[tag].add(id_tag)
    return tag_map

"""6. python.fancy_analytics"""
def count_fancy_views(stream: TextIO, default_view_count: int = 100500) -> dict[int: int]: 
    fancy_views = defaultdict(lambda: default_view_count)
    pattern_view = r'(?<=ViewCount=)"[0-9]+"'
    pattern_id = r'(?<=Id=)"[0-9]+"'
    for line in stream: 
        line = line.strip()
        if re.search(pattern_view, line) and re.search(pattern_id, line):
            id_tag = int(re.search(pattern_id, line).group().strip('"'))
            view_line = int(re.search(pattern_view, line).group().strip('"'))
            fancy_views[id_tag] += view_line
    return fancy_views

"""7. tag_generator"""
def generate_tags_from_stream(stream: TextIO) -> Iterator[str]:
    for line in stream:
        post = line.rstrip()
        for tag in generate_tags_from_post(post):
            yield tag
def generate_tags_from_post(stackoverflow_post: str) -> Iterator[str]:
    pattern_tags = r'(?<=Tags=")[^"]+'
    if re.search(pattern_tags, stackoverflow_post):
        clear_tags = list(re.search(pattern_tags, stackoverflow_post).group().replace('&lt;', ' ').replace('&gt;', ' ').split())
        for tag in clear_tags:
            yield tag
def build_tag_count_map(stream: TextIO) -> dict[str, int]:
    tag_counts = Counter(generate_tags_from_stream(stream))
    return tag_counts
