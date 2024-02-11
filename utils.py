import os

def write_urls_to_txt(file_path, urls, separator=" "):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(separator.join(urls))
        
def get_tags_str(tags):
    return " ".join(tags + [
        "-type:anime",
        "-female:scat_insertion",
        "-female:giantess",
        "-female:females_only",
        "-tag:western_cg",
        "-tag:western_imageset",
        "-tag:western_non-h",
        "-female:minigirl",
        "-male:miniguy",
        "-female:insect_girl",
        "-male:insect_boy",
        
        "-female:scat",
        "-male:scat",
        "-female:farting",
        "-male:farting",
        "-female:insect",
        "-male:insect",
        "-female:guro",
        "-male:guro",
        "-female:amputee",
        "-male:amputee",
        "-female:omorashi",
        "-male:omorashi",
        "-female:infantilism",
        "-male:infantilism",
        "-female:vore",
        "-male:vore",
        "-female:shrinking",
        "-male:shrinking",
        "-female:unbirth",
        "-male:unbirth",
        "-female:smell",
        "-male:smell",
        "-female:cbt",
        "-male:cbt",
        "-female:bdsm", # maybe disabel?
        "-male:bdsm",
        "-female:bondage",
        "-male:bondage",
        "-female:furry",
        "-male:furry",
        "-female:human_on_furry",
        "-male:human_on_furry",
        "-female:urination",
        "-male:urination",
        "-female:prolapse",
        "-male:prolapse",
        "-female:midget",
        "-male:midget",
        "-female:abortion",
        "-male:abortion",
        "-female:analphagia",
        "-male:analphagia",
        "-female:snuff",
        "-male:snuff",
        "-female:asphyxiation",
        "-male:asphyxiation",
    ])

def get_doujinshi_id_set_from_dir(dir_path):
    id_set = set()
    for dir_name in os.listdir(dir_path):
        id_set.add(dir_name[
            dir_name.find("(") + 1:
            dir_name.find(")")
        ])
    return id_set

def get_doujinshi_id_from_url(doujinshi_url):
    return doujinshi_url[
        doujinshi_url.rfind("-") + 1:
        doujinshi_url.rfind(".html")
    ]